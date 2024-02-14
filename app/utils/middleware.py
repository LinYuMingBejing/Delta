from abc import ABC, abstractmethod
from datetime import datetime
from flask import request
from typing import Optional

from constant import ALLOWED_MEDIA_TYPE, ALLOWED_REFERER, \
    ALLOWED_DOMAIN, ALLOWED_HOST, HEADER_FROM
from exception import AuthenticateException, HostException, \
    MediaTypeException, RefererException


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    _next_handler = None
    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def _check(self, request:request):
        pass

    def handle(self, request: request) -> str:
        self._check(request)
        if self._next_handler:
            return self._next_handler.handle(request)


class CookieHandler(AbstractHandler):
    def _check(self, request: request) -> str:
        cookie = request.cookies
        if not cookie:
            raise AuthenticateException()
        domain = request.cookies.get('domain')
        expires = request.cookies.get('expires')
        expires_timestamp = datetime.strptime(expires, "%a, %d %b %Y %H:%M:%S %Z").timestamp()
        if expires_timestamp < datetime.now().timestamp():
            raise AuthenticateException()
        if domain != ALLOWED_DOMAIN:
            raise AuthenticateException()


class QueryStringHandler(AbstractHandler):
    def _check(self, request: request) -> str:
        request.args = {}


class AgentValueHandler(AbstractHandler):
    def _check(self, request: request) -> str:
        agent_header = request.headers.get('X-DSEBD-AGENT')
        if not agent_header or not agent_header.startswith('AGENT_'):
            raise AuthenticateException()
        

class AgentHandler(AbstractHandler):
    def _check(self, request: request) -> str:
        agent_header = request.headers.get('X-DSEBD-AGENT')
        if not agent_header:
            raise AuthenticateException()


class ContentTypeHandler(AbstractHandler):
    def _check(self, request: request) -> str:
        content_type = request.headers.get('CONTENT-TYPE')
        if content_type != ALLOWED_MEDIA_TYPE:
            raise MediaTypeException()


class RefererHandler(AbstractHandler):
    def _check(self, request: request) -> str:
        referer = request.referrer
        if referer != ALLOWED_REFERER:
            raise RefererException()


class HeaderHandler(AbstractHandler):
    def _check(self, response) -> str:
        if request.path.startswith('/dsebd/api/v1'):
            response.headers['From'] = HEADER_FROM


class TimestampHandler(AbstractHandler):
    def _check(self, response) -> str:
        response.headers['X-DSEBD-TIMESTAMP'] = datetime.now()


class HostHandler(AbstractHandler):
    def _check(self, request: request) -> str:
        host = request.host.split(':')[0]
        if host != ALLOWED_HOST:
            raise HostException()
