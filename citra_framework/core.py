'''
Defines the main `Citra` application class.
Responsible to handle all services.
'''

from citra_framework.components.database import Database
from citra_framework.components.logger import Logger
from citra_framework.components.middleware import Middleware
from citra_framework.components.router import Router
from citra_framework.components.server import Server
from citra_framework.components.debugger import Debugger
from citra_framework.components.requests import Request
from citra_framework.components.response import Response
from citra_framework.components.template_engine.zest import Zest


class Citra:
    
    '''
    Core application Citra Framework
    --------------------------------
    
    Attributes:
        send (Router): manages routes and dispatching.
        middleware (Middleware): holds middleware functions.
        database (Database | None): optional database integration.
        logger (Logger): application-wide logging system.
    '''
    _DEFAULT_SOURCE_TEMPLATE = 'src'
    _DEFAULT_HOSTNAME = '127.0.0.1'
    _DEFAULT_PORT = 8000
    
    def __init__(
        self,
        enable_db=False,
        config_db=None,
        debug=False,
        template_dir=_DEFAULT_SOURCE_TEMPLATE
    ):
        
        '''
        Intialize `Citra` application.
        
        Args:
            enable_db (bool | optional): initialize database connection `(MySQL)`.
            db_config (dict | optional): connection details (`host`, `username`, `password`, `database`).
            debug (bool): debugging mode for development.
        '''
        
        self.router = Router()
        self.middleware = Middleware()
        self.logger = Logger()
        self.debugger = Debugger(enabled=debug, logger=self.logger)
        self.debug = debug
        self.database = None 
        self._default_page = None
        
        # --- template engine
        self.templates = Zest(template_dir, router=self.router)
        
        
        # --- Initializing citra app ---
        if debug:
            self.logger.debug('DEBUG mode is ON.')
        else:
            self.logger.warning('Starting Citra Development...')
        
        # --- Condition if database integration is enable. ---
        if enable_db:
            configure = config_db or {}
            self.database = Database(
                hostname=configure.get('hostname', 'localhost'),
                username=configure.get('username', 'root'),
                password=configure.get('password', ''),
                database=configure.get('database', '')
            )
    
    def send(
        self,
        path,
        handler,
        method='GET',
        name=None
    ):
        
        '''
        Register a new route.
        
        Args:
            path (str): URL path (e.g., '/').
            handler (coroutine): function to handle the request.
            method (str, optional): HTTP method defaults to 'GET'.
            name (str, optional): name for reverse route lookup.
        '''
        
        self.router.send(path, handler, method, name)
        
    def serve(
        self,
        host=_DEFAULT_HOSTNAME,
        port=_DEFAULT_PORT
    ):
        
        '''
        Start the HTTP server.
        
        Args:
            host (str, optional): host to bind defaults to `'127.0.0.1'`.
            port (int, optional): port to bind defaults to `8000`.
        '''
        
        server = Server(self, host, port)
        server.serve()