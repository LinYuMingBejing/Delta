class CodeDefinition:
    def __init__(self, code, message):
        self.code = code
        self.__message = message

    @property
    def message(self):
        return self.__message

    def format_message(self, **kwargs):
        if kwargs:
            return self.__message.format(**kwargs)
        return self.__message
    

SUCCESS = CodeDefinition(200, 'The action was performed successfully.')
RESOURCE_NOT_FOUND = CodeDefinition(404, 'Resource not found.')
UNEXPECTED_ERROR = CodeDefinition(500, 'An unexpected error has occurred.')
REDIRECT = CodeDefinition(302, 'Redirect successfully.')
BAD_REQUEST = CodeDefinition(400, 'Bad request.')
UNAUTHORIZED = CodeDefinition(401, 'Unauthorized.')
FORBIDDEN = CodeDefinition(403, 'Forbidden.')
UNSUPPORTED_MEDIA_TYPE = CodeDefinition(415, 'Unsupported media type.')
