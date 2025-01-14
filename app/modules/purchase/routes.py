from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app.models import Purchase
from app import db, logger
from app.utils.is_admin import is_admin
from . import module, forms


# get current purchases
@module.route('/', methods=['GET'])
@is_admin
@login_required
def purchase():
    form = forms.CreatePurchaseForm()
    purchases = Purchase.query.all()

    return render_template('purchase/purchase.html', title='План закупок', purchases=purchases, form=form)

# create new purchase
@module.route('/create', methods=['POST'])
@is_admin
@login_required
def create_purchase():
    form = forms.CreatePurchaseForm()

    if form.validate_on_submit():
        try:
            purchase: Purchase = Purchase(name=form.name.data,
                                          quantity=form.quantity.data,
                                          price=form.price.data,
                                          supplier=form.supplier.data)
            db.session.add(purchase)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating new purchase: {e}")
            flash('Произошла ошибка!', 'error')
    return redirect(url_for('purchase.purchase'))