class DeltaException(Exception):
    def __init__(self, message='', context=None):

        super().__init__(message)
        self.message = message

        if message:
            self.message = message

        if context:
            self.context = context
        else:
            self.context = {}


class AuthenticateException(Exception):
    def __init__(self, message='', context=None):
        super().__init__(message)


class RefererException(Exception):
    def __init__(self, message='', context=None):
        super().__init__(message)


class MediaTypeException(Exception):
    def __init__(self, message='', context=None):
        super().__init__(message)


class HostException(Exception):
    def __init__(self, message='', context=None):
        super().__init__(message)
