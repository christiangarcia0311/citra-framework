from citra_framework.components.middleware import BaseMiddleware
from citra_framework.components.response import Response

class CorsMiddleware(BaseMiddleware):
    
    '''
    Middleware for handling Cross-Origin Resource Sharing (CORS).
    
    Automatically attaches the required CORS headers to HTTP response
    allowing the client applications from different origins to interact
    with the server safely.
    
    Typically used in  API's where requests may come from browsers hosted
    on sseparate domains.
    
    Args:
        allow_oigin (str): allowed origin (default: `*`).
        allow_methods (list[str]): allowed HTTP methods permitted (default: GET, POST, PUT< DELETE, OPTIONS).
        allow_headers (list[str]): allowed request headers (default: Content-Type, Authorization).
    '''
    
    def __init__(
        self,
        allow_origin='*',
        allow_methods=None,
        allow_headers=None
    ):
        self.allow_origin = allow_origin
        self.allow_methods = allow_methods or ['GET', 'POST', 'PUT', 'DELETE']
        self.allow_headers = allow_headers or ['Content-Type', 'Authorization']
        
    async def process_request(self, request, handler):
        
        '''
        Process an incoming request and apply CORS policies.
        
        Args:
            request (Request): incoming HTTP request object.
            handler (callable): the route handler to process the request.
        '''
        
        route_config = getattr(request, 'cors', None)
        
        allow_origin = route_config.get('origin', self.allow_origin) if route_config else self.allow_origin
        allow_methods = route_config.get('methods', self.allow_methods) if route_config else self.allow_methods
        allow_headers = route_config.get('headers', self.allow_headers) if route_config else self.allow_headers

        response = handler(request)
        
        # --- make it always response ---
        if not isinstance(response, Response):
            response = Response(response)
            
        # --- inject headers ---
        response.headers['Access-Control-Allow-Origin'] = allow_origin
        response.headers['Access-Control-Allow-Methods'] = ', '.join(allow_methods)
        response.headers['Access-Control-Allow-Headers'] = ', '.join(allow_headers)
        
        return response
        