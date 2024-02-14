from flask import request, jsonify
from marshmallow import ValidationError

from app.api import api
from models import Size
from schema import SizeSchema
from settings.defaults import SQLALCHEMY_BINDS
from tasks import db_sync
from utils.message import QueueMessage
from utils.method import METHOD
from utils.status import SUCCESS


@api.route('/size')
def queryAllSize():
    sizes = [row.to_dict() for row in Size.query.all()]
    return jsonify(data=sizes, code=200)


@api.route('/size/<size_id>')
def querySize(size_id):
    size = Size.query.get_or_404(size_id)
    return jsonify(data=size.to_dict(), code=200)


@api.route('/size', methods=['POST'])
def createSize():
    data = request.json
    try:
        SizeSchema().load(data)
    except ValidationError as err:
        return jsonify(message=err.messages, code=422), 422
   
    size = Size()
    size.name = data['name']
    size.save()

    db_sync.delay(QueueMessage(
        'Size',
        size.to_dict(),
        METHOD.POST.name, 
        SQLALCHEMY_BINDS['internal_database']).to_dict()
    )

    return jsonify(data=size.to_dict(), message=SUCCESS.message, code=201)


@api.route('/size/<size_id>', methods=['PUT'])
def updateSize(size_id):
    data = request.json
    try:
        SizeSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    size = Size.query.get_or_404(size_id)
    size.name = data['name']
    size.save()

    db_sync.delay(QueueMessage(
        'Size',
        size.to_dict(), 
        METHOD.PUT.name, 
        SQLALCHEMY_BINDS['internal_database']).to_dict()
    )

    return jsonify(data=size.to_dict(), message=SUCCESS.message, code=201)


@api.route('/size/<size_id>', methods=['DELETE'])
def deleteSize(size_id):    
    size = Size.query.get_or_404(size_id)
    size.delete()

    db_sync.delay(QueueMessage(
        'Size',
        size.to_dict(), 
        METHOD.DELETE.name, 
        SQLALCHEMY_BINDS['internal_database']).to_dict()
    )

    return jsonify(data=size.to_dict(), message=SUCCESS.message, code=201)
