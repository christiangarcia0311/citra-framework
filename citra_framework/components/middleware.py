class BaseMiddleware:
    
    '''
    Base class for all `Citra` middlewares.
    Provides consistent interface for request processing.
    '''
    
    async def process_request(self, request, handler):
        
        ''' Must be overriden by child middleware. '''
        
        raise NotImplementedError('Middleware must be implement process_request() function.')

class Middleware:
    
    '''
    Initialize middleware manager for `Citra`
    
    Allows registering and chaining middleware classes.
    
    Middleware must implement:
        async def proceess_request(self, request, handler): ...
    '''
    
    def __init__(self):
        
        '''
        Attributes:
            functions (list): registered middleware functions.
        '''
        
        self.middlewares = []
        
    def add(self, func):
        
        '''
        Register a middleware function.
        
        Args:
            func (callable): function accepting (request, next).
        '''
        
        self.middlewares.append(func)
        
    def _wrap(self, middleware, handler):
        async def wrapper(request):
            return await middleware.process_request(request, handler)
        
        return wrapper
        
    async def run(self, request, handler):
        
        '''
        Run requeest through middleware chain.
        
        Args:
            request (Request): current request.
            handler ():
        '''
        
        for middleware in reversed(self.middlewares):
            handler = self._wrap(middleware, handler)
        
        return await handler(request)