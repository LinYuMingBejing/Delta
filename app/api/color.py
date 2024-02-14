from flask import jsonify, request
from marshmallow import ValidationError

from app.api import api
from models import Color
from schema import ColorSchema
from settings.defaults import SQLALCHEMY_BINDS
from tasks import db_sync
from utils.message import QueueMessage
from utils.method import METHOD
from utils.status import SUCCESS


@api.route('/color')
def queryAllColor():
    colors = [row.to_dict() for row in Color.query.all()]
    return jsonify(data=colors, code=200)


@api.route('/color/<color_id>')
def queryColor(color_id):
    color = Color.query.get_or_404(color_id)
    return jsonify(data=color.to_dict(), code=200)


@api.route('/color', methods=['POST'])
def createColor():
    data = request.json
    try:
        ColorSchema().load(data)
    except ValidationError as err:
        return jsonify(message=err.messages, code=422), 422
   
    color = Color()
    color.name = data['name']
    color.save()

    db_sync.delay(QueueMessage(
        'Color',
        color.to_dict(),
        METHOD.POST.name, 
        SQLALCHEMY_BINDS['internal_database']).to_dict()
    )

    return jsonify(data=color.to_dict(), message=SUCCESS.message, code=201)


@api.route('/color/<color_id>', methods=['PUT'])
def updateColor(color_id):
    data = request.json
    try:
        ColorSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422
   
    color = Color.quert.get_or_404(color_id)   
    color.name = data['name']
    color.save()

    db_sync.delay(QueueMessage(
        'Color',
        color.to_dict(),
        METHOD.PUT.name, 
        SQLALCHEMY_BINDS['internal_database']).to_dict()
    )

    return jsonify(data=color.to_dict(), message=SUCCESS.message, code=201)


@api.route('/color/<color_id>', methods=['PUT'])
def deleteColor(color_id):
    color = Color.quert.get_or_404(color_id)
    color.delete()

    db_sync.delay(QueueMessage(
        'Color',
        color.to_dict(),
        METHOD.DELETE.name, 
        SQLALCHEMY_BINDS['internal_database']).to_dict()
    )

    return jsonify(data=color.to_dict(), message=SUCCESS.message, code=201)
