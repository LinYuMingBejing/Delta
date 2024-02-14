from flask import jsonify, request
from marshmallow import ValidationError

from app import db
from app.api import api
from models import Inventory, ClothInfo, Size, Color
from schema import InventorySchema
from utils.status import SUCCESS


@api.route('/inventory/cloth/<cloth_id>')
def queryCertainClothQuantity(cloth_id):
    rows = db.session.query(Inventory, ClothInfo, Size, Color).\
        join(ClothInfo, Inventory.cloth_id == ClothInfo.id).\
        join(Size, Inventory.size_id == Size.id).\
        join(Color, Inventory.color_id == Color.id).\
        filter(ClothInfo.id == cloth_id).all()
    data = []
    for row in rows:
        inventory, cloth, size, color = row
        data.append({
            'inventory_id': inventory.id,
            'cloth_name': cloth.name,
            'size_name': size.name,
            'color_name': color.name,
            'inventory': inventory.quantity
        })

    return jsonify(data=data, code=200)


@api.route('/inventory', methods=['POST'])
def createInventory():
    data = request.json
    try:
        InventorySchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    if not Size.query.get(data['size_id']):
        return jsonify(message='Invalid size_id', code=422), 422
    if not Color.query.get(data['color_id']):
        return jsonify(message='Invalid color_id', code=422), 422
    if not ClothInfo.query.get(data['cloth_id']):
        return jsonify(message='Invalid cloth_id', code=422), 422
   
    inventory = Inventory()
    inventory.cloth_id = data['cloth_id']
    inventory.color_id = data['color_id']
    inventory.size_id = data['size_id']
    inventory.quantity = data['quantity']
    inventory.save()

    return jsonify(data=inventory.to_dict(), message=SUCCESS.message, code=200)


@api.route('/inventory/<inventory_id>', methods=['PUT'])
def updateInventory(inventory_id):
    data = request.json
    try:
        InventorySchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    if not Size.query.get(data['size_id']):
        return jsonify(message='Invalid size_id', code=422), 422
    if not Color.query.get(data['color_id']):
        return jsonify(message='Invalid color_id', code=422), 422
    if not ClothInfo.query.get(data['cloth_id']):
        return jsonify(message='Invalid cloth_id', code=422), 422
    
    inventory = Inventory.query.get_or_404(inventory_id)
    inventory.cloth_id = data['cloth_id']
    inventory.color_id = data['color_id']
    inventory.size_id = data['size_id']
    inventory.quantity = data['quantity']
    inventory.save()

    return jsonify(data=inventory.to_dict(), message=SUCCESS.message, code=200)


@api.route('/inventory/<inventory_id>', methods=['DELETE'])
def deleteInventory(inventory_id):    
    inventory = Inventory.query.get_or_404(inventory_id)
    inventory.delete()
    return jsonify(data=inventory.to_dict(), code=201), 201
