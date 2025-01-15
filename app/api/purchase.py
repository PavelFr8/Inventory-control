from flask import request, jsonify

from app import db
from app.models import Purchase
from app.utils.json_is_valid import json_is_valid
from . import module


@module.route('/create_purchase', methods=['POST'])
@json_is_valid({"name": str, "quantity": int, "price": int, "supplier": str})
def create_purchase():
    """
    Creates a new purchase.

    Request JSON body:
        - name (str): The name of the item in purchase.
        - supplier (str): The name of the supplier.
        - price (int): The planning price of inventory item
        - quantity (int): The quantity of the item in purchase.

    :return: JSON response:
        - status (str): 'success' if the device is purchase successfully.
        - HTTP status code 201.
    """
    try:
        name = request.json['name']
        supplier = request.json['supplier']
        price = request.json['price']
        quantity = request.json['quantity']

        # Create new purchase
        purchase: Purchase = Purchase(name=name, quantity=quantity, price=price, supplier=supplier)

        db.session.add(purchase)
        db.session.commit()

        return jsonify({"status": "success"}), 201
    except:
        return jsonify({"status": "error", "message": "Error while creating purchase"}), 400


@module.route('/delete_purchase', methods=['DELETE'])
@json_is_valid({"id": int})
def delete_purchase():
    """
    Delete purchase.

    Request JSON body:
        - id (int): ID of purchase.

    :return: JSON response:
        - status (str): 'success' if the device deleted successfully.
        - HTTP status code 201.
    """
    try:
        id = request.json['id']

        purchase: Purchase = Purchase.query.get(id)

        db.session.delete(purchase)
        db.session.commit()

        return jsonify({"status": "success"}), 201
    except:
        return jsonify({"status": "error", "message": "Error while creating purchase"}), 400
