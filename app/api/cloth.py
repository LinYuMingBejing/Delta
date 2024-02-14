from flask import jsonify, request
from marshmallow import ValidationError

from app.api import api
from models import Category, ClothInfo
from schema import ClothInfoSchema
from settings.defaults import SQLALCHEMY_BINDS
from tasks import db_sync
from utils.message import QueueMessage
from utils.method import METHOD
from utils.status import SUCCESS


@api.route('/cloth')
def queryAllCloth():
    clothes = [row.to_dict() for row in ClothInfo.query.all()]
    return jsonify(data=clothes, code=200)


@api.route('/cloth/<cloth_id>')
def queryCloth(cloth_id):
    cloth = ClothInfo.query.get_or_404(cloth_id)
    return jsonify(data=cloth.to_dict(), code=200)


@api.route('/cloth', methods=['POST'])
def createClothInfo():
    data = request.json
    try:
        ClothInfoSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    if not Category.query.get(data['category_id']):
        return jsonify(message='Invalid category_id', code=422), 422
    
    cloth = ClothInfo()
    cloth.code = data['code']
    cloth.name = data['name']
    cloth.unit_price = data['unit_price']
    cloth.category_id = data['category_id']
    cloth.save()

    db_sync.delay(QueueMessage(
        'ClothInfo',
        cloth.to_dict(),
        METHOD.POST.name,
        SQLALCHEMY_BINDS['external_database']).to_dict()
    )

    return jsonify(data=cloth.to_dict(), message=SUCCESS.message, code=201), 201


@api.route('/cloth/<cloth_id>', methods=['PUT'])
def updateClothInfo(cloth_id):
    data = request.json
    try:
        ClothInfoSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    if not Category.query.get(data['category_id']):
        return jsonify(message='Invalid category_id', code=422), 422
    
    cloth = ClothInfo.query.get_or_404(cloth_id)
    
    cloth.code = data['code']
    cloth.name = data['name']
    cloth.unit_price = data['unit_price']
    cloth.category_id = data['category_id']
    cloth.save()

    db_sync.delay(QueueMessage(
        'ClothInfo',
        cloth.to_dict(),
        METHOD.PUT.name,
        SQLALCHEMY_BINDS['external_database']).to_dict()
    )

    return jsonify(data=cloth.to_dict(), message=SUCCESS.message, code=201), 201
