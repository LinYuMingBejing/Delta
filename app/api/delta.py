from flask import jsonify, request, redirect, url_for
from app.api import api
from utils.status import SUCCESS, REDIRECT


@api.route('/test_connection', methods=['GET'])
def echo():
    return jsonify(message=SUCCESS.message, code=200)


@api.route('/dsebd/api/v1/resource')
def orginRoute():
    return redirect(url_for('api.routeRedirect'))


@api.route('/dsebd/api/v1/sta')
def routeRedirect():
    return jsonify(path=request.path, message=REDIRECT.message, code=302), 302
