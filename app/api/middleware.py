from flask import request, jsonify

from app.api import api
from constant import WHITE_LIST
from utils.method import METHOD
from utils.middleware import AgentHandler, AgentValueHandler, ContentTypeHandler, CookieHandler,\
    HostHandler, HeaderHandler, QueryStringHandler, RefererHandler, TimestampHandler
from utils.status import UNAUTHORIZED, FORBIDDEN, UNSUPPORTED_MEDIA_TYPE, BAD_REQUEST
from exception import AuthenticateException, RefererException, MediaTypeException, HostException


def excludeWhileList(func):
    def wrapper():
        if request.path != WHITE_LIST:
            return func()
    return wrapper


@api.before_request
@excludeWhileList
def commonRequestMiddleware():
    try:
        HostHandler().handle(request)
    except HostException:
        return jsonify(message=BAD_REQUEST.message, code=BAD_REQUEST.code), 400
    

@api.after_request
def commonResponseMiddleware(response):
    TimestampHandler().handle(response)
    return response


@api.before_request
def methodPOSTRequestMiddleware():
    if request.method != METHOD.POST.name or request.method != METHOD.PUT.name:
        return
    
    try:
        queryStringChecker = QueryStringHandler()
        agentChecker = AgentHandler()
        contentTypeChecker = ContentTypeHandler()

        queryStringChecker.set_next(agentChecker)
        agentChecker.set_next(contentTypeChecker)
        
        queryStringChecker.handle(request)
    except MediaTypeException:
        return jsonify(message=UNSUPPORTED_MEDIA_TYPE.message, code=UNSUPPORTED_MEDIA_TYPE.code), 415
    except AuthenticateException:
        return jsonify(message=UNAUTHORIZED.message, code=UNAUTHORIZED.code), 401


@api.before_request
@excludeWhileList
def methodGetRequestMiddleware():
    if request.method != METHOD.GET.name:
        return
    try:
        cookieChecker = CookieHandler()
        refererChecker = RefererHandler()
        cookieChecker.set_next(refererChecker)
        cookieChecker.handle(request)
    except AuthenticateException:
        return jsonify(message=UNAUTHORIZED.message, code=UNAUTHORIZED.code), 401
    except RefererException:
        return jsonify(message=FORBIDDEN.message, code=FORBIDDEN.code), 403
    except Exception as err:
        print(str(err))


@api.after_request
def methodGetResponseMiddleware(response):
    if request.method  == METHOD.GET.name:
        HeaderHandler().handle(response)
    return response


@api.before_request
def methodDeleteRequestMiddleware():
    if request.method != METHOD.DELETE.name:
        return
    try:
        AgentValueHandler().handle(request)
    except AuthenticateException:
        return jsonify(message=UNAUTHORIZED.message, code=UNAUTHORIZED.code), 401
