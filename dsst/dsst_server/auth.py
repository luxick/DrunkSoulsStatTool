READ_TOKENS = []
WRITE_TOKENS = []


class AuthenticationError(Exception):
    def __init__(self, message):
        self.message = message

    def get_response(self):
        return {
            'success': False,
            'message': 'Authentication Failed:\n'.format(self.message)
        }


def check_read(func):
    def wrapper(*args, **kwargs):
        token = args[0]
        if token in READ_TOKENS + WRITE_TOKENS:
            return func(*args[1:], **kwargs)
        else:
            raise AuthenticationError('Token "{}" has no read access on database.'.format(token))
    return wrapper


def check_write(func):
    def wrapper(*args, **kwargs):
        token = args[0]
        if token in WRITE_TOKENS:
            return func(*args[1:], **kwargs)
        else:
            raise AuthenticationError('Token "{}" has no write access on database.'.format(token))
    return wrapper
