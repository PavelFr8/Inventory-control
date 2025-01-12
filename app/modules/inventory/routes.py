from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from app.models import Item, ItemState, User
from app import db, logger
from app.utils.is_admin import is_admin
from . import module, forms


# shows items
@module.route('/my_inventory', methods=['GET'])
@login_required
def my_inventory():
    items = []
    available_items = []
    users = []
    form = forms.CreateItemForm()
    form2 = forms.ChangeItemForm()
    form3 = forms.AssignItemForm()

    if current_user.role.name == 'admin':
        items = Item.query.all()
        users = [user for user in User.query.all() if user.role.name != 'admin']
    if current_user.role.name == 'user':
        items = Item.query.filter_by(take_user_id=current_user.id).all()
        available_items = Item.query.filter_by(take_user_id=None).all()


    form3.user_id.choices = [(user.id, user.name) for user in users]
    form3.user_id.choices.insert(0, (0, "-"))

    return render_template('inventory/my_inventory.html', title='Доступный инвентарь', items=items, form=form,
                           form2=form2, form3=form3, users=users, available_items=available_items)

# adding new item to db
@module.route('/add_item', methods=['POST'])
@login_required
@is_admin
def add_item():
    form = forms.CreateItemForm()

    if form.validate_on_submit():
        logger.debug(f"Processing new inventory item: {form.name.data}")
        try:
            item = Item(
                name=form.name.data,
                quantity=form.quantity.data
            )
            db.session.add(item)
            db.session.commit()
            logger.info(f"Item {form.name.data} successfully added.")
            return redirect(url_for('inventory.my_inventory'))
        except Exception as e:
            logger.error(f"Error adding item {form.name.data}: {e}")
            db.session.rollback()
            return render_template('inventory/my_inventory.html', title='Доступный инвентарь', form=form,
                                   message='Произошла непредвиденная ошибка.')

# changing infp about item in db
@module.route('/change_item/<int:id>', methods=['POST'])
@login_required
@is_admin
def change_item(id):
    form = forms.ChangeItemForm()

    if form.validate_on_submit():
        logger.debug(f"Processing changing inventory item: {form.name.data}")
        try:
            if form.state.data == 'new':
                form.state.data = ItemState.NEW
            elif form.state.data == 'used':
                form.state.data = ItemState.USED
            elif form.state.data == 'broken':
                form.state.data = ItemState.BROKEN

            item: Item = Item.query.get(id)
            item.name = form.name.data
            item.quantity = form.quantity.data
            item.state = form.state.data
            db.session.commit()
            logger.info(f"Item {form.name.data} successfully added.")

            return redirect(url_for('inventory.my_inventory'))
        except Exception as e:
            logger.error(f"Error adding item {form.name.data}: {e}")
            db.session.rollback()
            return render_template('inventory/my_inventory.html', title='Доступный инвентарь', form=form,
                                   message='Произошла непредвиденная ошибка.')

# deleting item from db
@module.route('/delete_item/<int:id>')
@login_required
@is_admin
def delete_item(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    logger.debug(f"Successfully delete item {item.name}")
    return redirect(url_for('inventory.my_inventory'))


# assigning item to user
@module.route('/assign_item/<int:id>', methods=['POST'])
@login_required
@is_admin
def assign_item(id):
    form = forms.AssignItemForm()
    users = [user for user in User.query.all() if user.role.name != 'admin']

    form.user_id.choices = [(user.id, user.name) for user in users]
    form.user_id.choices.insert(0, (0, "-"))

    if form.validate_on_submit():
        try:
            item: Item = Item.query.get(id)

            item.take_user_id = form.user_id.data if form.user_id.data != "0" else None
            db.session.commit()

            logger.info(f"Item {item.name} assigned to user ID {form.user_id.data}.")
            return redirect(url_for('inventory.my_inventory'))
        except Exception as e:
            logger.error(f"Error assigning item {id}: {e}")
            db.session.rollback()
            return redirect(url_for('inventory.my_inventory', message='Произошла ошибка назначения.'))
