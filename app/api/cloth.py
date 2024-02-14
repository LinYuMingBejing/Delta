from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from app.api import api
from models import Category, ClothInfo
from schema import ClothInfoSchema
from utils.status import SUCCESS


@api.route('/cloth', methods=['POST'])
def createClothInfo():
    data = request.json
    try:
        ClothInfoSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    if not Category.query.get(data['category_id']):
        raise ValidationError({'category_id': 'Invalid category_id'})
    
    cloth = ClothInfo()
    cloth.code = data['code']
    cloth.name = data['name']
    cloth.unit_price = data['unit_price']
    cloth.category_id = data['category_id']
    cloth.save()

    return jsonify({"result": cloth.to_dict()}), 201


@api.route('/cloth/<cloth_id>', methods=['PUT'])
def updateClothInfo(cloth_id):
    data = request.json
    try:
        ClothInfoSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    cloth = ClothInfo.query.get(cloth_id)

    if not cloth:
        raise NoResultFound
    
    if not Category.query.get(data['category_id']):
        raise ValidationError({'category_id': 'Invalid category_id'})
    
    cloth.code = data['code']
    cloth.name = data['name']
    cloth.unit_price = data['unit_price']
    cloth.category_id = data['category_id']
    cloth.save()

    return jsonify(data=cloth.to_dict(), message=SUCCESS.message, code=200)
