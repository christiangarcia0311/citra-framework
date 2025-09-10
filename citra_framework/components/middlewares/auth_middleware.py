from citra_framework.components.middleware import BaseMiddleware
from citra_framework.components.error_pages.error import UnauthorizedError

def protected_route(handler):
    
    handler.is_protected = True
    return handler

class AuthenticationMiddleware(BaseMiddleware):
    
    '''
    Middleware for handling simple  request authentication.
    Attaches request.user (None if unauthenticated).
    '''
    pass