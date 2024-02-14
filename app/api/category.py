from flask import jsonify, request
from marshmallow import ValidationError

from app.api import api
from models import Category
from schema import CategorySchema
from settings.defaults import SQLALCHEMY_BINDS
from tasks import db_sync
from utils.message import QueueMessage
from utils.method import METHOD
from utils.status import SUCCESS


@api.route('/category')
def queryAllCategory():
    categories = [row.to_dict() for row in Category.query.all()]
    return jsonify(data=categories, code=200)


@api.route('/category/<category_id>')
def queryCategory(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify(data=category.to_dict(), code=200)


@api.route('/category', methods=['POST'])
def createCategory():
    data = request.json
    try:
        CategorySchema().load(data)
    except ValidationError as err:
        return jsonify(message=err.messages, code=422), 422
    
    category = Category()
    category.name = data['name']
    category.save()

    db_sync.delay(QueueMessage(
        'Category',
        category.to_dict(), 
        METHOD.POST.name, 
        SQLALCHEMY_BINDS['external_database']).to_dict()
    )

    return jsonify(data=category.to_dict(), code=201), 201


@api.route('/category/<category_id>', methods=['PUT'])
def updateCategory(category_id):
    data = request.json
    try:
        CategorySchema().load(data)
    except ValidationError as err:
        return jsonify(message=err.messages, code=422), 422
    
    category = Category.query.get_or_404(category_id)    
    category.name = data['name']
    category.save()

    db_sync.delay(QueueMessage(
        'Category',
        category.to_dict(), 
        METHOD.PUT.name, 
        SQLALCHEMY_BINDS['external_database']).to_dict()
    )

    return jsonify(data=category.to_dict(), message=SUCCESS.message, code=200)


@api.route('/category/<category_id>', methods=['DELETE'])
def deleteCategory(category_id):
    category = Category.query.get_or_404(category_id)
    category.delete()
    
    db_sync.delay(QueueMessage(
        'Category',
        category.to_dict(), 
        METHOD.DELETE.name, 
        SQLALCHEMY_BINDS['external_database']).to_dict()
    )

    return jsonify(data=category.to_dict(), message=SUCCESS.message, code=200)
