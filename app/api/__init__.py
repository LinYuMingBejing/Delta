from flask import Blueprint

api = Blueprint('api', __name__)

from . import category, cloth, color, inventory, size, delta, middleware
