from citra_framework.components.response import Response 
from citra_framework.components.error_pages.error import NotFoundError
import re 

class Router:
    
    '''
    Router class for mapping HTTP requests to its corresponding handlers.
    
    This class provides `route registration`, `reverse URL lookup` and `request
    dispatching`. It supports static and dynamic URL segments using `regex` patterns.
    
    Responsibilities:
        - register routes with HTTP methods and optional names.
        - support dynamic segments (e.g., `/users/<user_id>`).
        - enable reverse URL generation via named routes.
        - dispatching incoming requests to correct handler.
        - return a 404 error page when no route matchers.
        
        
    Example:
    
        router = Route()
        
        # register a route
        async def get_user_info(request, user_id):
            return Response(f'user {user_id}')
        
        async def list_of_users(request):
            return Response(f'user list.')
            
        router.send('/users/<user_id>', get_user_info, method='GET')
        
        # using cors
        router.send(
            '/user_list',
            list_of_users,
            method='GET',
            'headers': ['Authorization']
        )
        
        # reverse lookup
        path = router.url_route('user_details', id=12)
        
        # dispatching a request
        response =  await router.dispatch(request, app)
    '''
    
    def __init__(self):
        
        '''
        Initialize routes.
        
        Attributes:
            routes (list[tuple]): a list of registered route as tuples of (regex_pattern, handler, method).
            named_routes (dict): a dictionary mapping route names to its registered paths for reverse lookups.
        '''
        
        self.routes = []
        self.named_routes = {}
    
    def send(
        self,
        path,
        handler,
        method='GET',
        name=None,
        cors=None
    ):
        
        '''
        Register a new route.
        
        Args:
            path (str): URL path `/` `/users`.
            handler (coroutine): function to handle a request.
            method (str): HTTP method `(GET, POST, etc..)`.
            name (str, optional): route name for reverse lookup.
        '''
        
        pattern = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', path)
        regex = re.compile(f'^{pattern}$')
        self.routes.append((regex, handler, method, cors))
        
        
        # --- if no route name is given, default to handler name ---
        route_name = name or handler.__name__
        self.named_routes[route_name] = path
        
    def url_route(self, name, **kwargs):
        
        '''
        Generate URL from a named route.
        
        Args:
            name (str): route name.
            **kwargs: values to replace dynamic segments in the path.
            
        Returns:
            str: constructed URL.
        '''
        
        if name not in self.named_routes:
            raise KeyError(f'Route name: {name} not found')
        
        path = self.named_routes[name]
        for key, value in kwargs.items():
            path = path.replace(f'<{key}>', str(value))
        
        return path
    
    async def dispatch(self, request, app):
        
        '''
        Match an incoming request to a registered route and call its handler.
        
        Args:
            request (Request): parsed HTTP request.
            app (Citra): app instance.
        '''
        
        for regex, handler, method, cors in self.routes:
            if request.method == method:
                match = regex.match(request.path)
                if match:
                    kwargs = match.groupdict()
                    # request.cors
                    if cors:
                        request.headers['Access-Control-Allow-Origin'] = '*'
                    return await handler(request, **kwargs)
        
        return NotFoundError(details=f'Method: {request.method} Request Path: {request.path} not found.', debug=app.debug).display()