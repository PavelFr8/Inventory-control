from flask import request, jsonify
from app import db, logger
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
        - price (int): The planning price of inventory item.
        - quantity (int): The quantity of the item in purchase.

    :return: JSON response:
        - status (str): 'success' if the purchase is created successfully.
        - HTTP status code 201.
    """
    try:
        name = request.json['name']
        supplier = request.json['supplier']
        price = request.json['price']
        quantity = request.json['quantity']

        # Validate input values
        if price <= 0:
            return jsonify({"status": "error", "message": "Price must be greater than zero"}), 400
        if quantity < 0:
            return jsonify({"status": "error", "message": "Quantity cannot be negative"}), 400

        # Create new purchase
        purchase = Purchase(name=name, quantity=quantity, price=price, supplier=supplier)

        db.session.add(purchase)
        db.session.commit()

        return jsonify({"status": "success", "id": purchase.id}), 201
    except Exception as e:
        logger.error(f"Error while creating purchase: {e}. Request data: {request.json}")
        return jsonify({"status": "error", "message": "Error while creating purchase"}), 500


@module.route('/delete_purchase', methods=['DELETE'])
@json_is_valid({"id": int})
def delete_purchase():
    """
    Delete a purchase.

    Request JSON body:
        - id (int): ID of the purchase.

    :return: JSON response:
        - status (str): 'success' if the purchase is deleted successfully.
        - HTTP status code 200.
    """
    try:
        id = request.json['id']

        purchase = Purchase.query.get(id)

        if not purchase:
            return jsonify({"status": "error", "message": f"Purchase with ID {id} not found"}), 404

        db.session.delete(purchase)
        db.session.commit()

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Error while deleting purchase: {e}. Request data: {request.json}")
        return jsonify({"status": "error", "message": "Error while deleting purchase"}), 500
