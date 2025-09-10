from citra_framework.components.requests import Request
from citra_framework.components.response import Response
import asyncio 
from colorama import Fore, Style

class Server:
    
    '''
    Asynchronous HTTP server class for `Citra` framework.
    
    This server manage `client connections`, `parses incoming HTTP requests`,
    `delegates them to the router` for handling and `sends responses` back to
    the client. It is designed for development use and not optimized for production environments.
    
    Responsibilities:
        - accept client connections using `asyncio`.
        - parse raw `HTTP requests` into `Request` objects.
        - dispatch requests to the router for response generation.
        - manage the event loop for contionous serving until shutdown.
        
    Attributes:
        app (Citra): the `citra` application instance.
        host (str): host address to bind (default `'127.0.0.1'`).
        port (int): port number to bind (default `8000`)
        
    Example:
        from citra_framework.components.server import Server
        from citra_framework.core import Citra
        
        app = Citra()
        
        server = Server(app, host='0.0.0.0', port=8000)
        server.serve()
        
    Notes:
        - Tthis server is intended for development only. for production, production -ready
          WSGI/ASGI server (e.g., Gunicorn, Uvicorn).
        - Exceptions raised during requests handling are passed to the app debugger for 
          consistent error reporting.
    '''
    
    def __init__(
        self,
        app,
        host='127.0.0.1',
        port=8000
    ):
        
        '''
        Initialize server instance.
        
        Args:
            app (Citra): the `Citra` application.
            host (str, optional): host address.
            port (int, optional): port number default to `8000`.
        '''
        
        self.app = app
        self.host = host
        self.port = port
    
    async def handle_client(self, reader, writer):
        
        '''
        Handle an incoming client connection.
        
        Args:
            reader (StreamReader): async stream reader.
            writer (StreamWriter): async stream writer.
            
        Flow:
            - Read request from client.
            - Parse into request object.
            - Dispatch to router for response.
            - Write back response to client.
            - Handle errors with 500 response code.
        '''
        
        try:
            data = await reader.read(1024)
            
            if not data:
                return

            request = Request.parse(data)
            response = await self.app.router.dispatch(request, self.app)
            self.app.logger.info(f'{request.method} {request.path} {response.status_code}')
            writer.write(response.build())
            await writer.drain()
            
        except Exception as e:
            response = self.app.debugger.handle_exception(e)
            writer.write(response.build())
            await writer.drain()
            
        finally:
            writer.close()
            await writer.wait_closed()
    
    def serve(self):
        
        '''
        Start the HTTP server and keep it running.
        
        This method creates an asyncio-based TCP server bound to the configured
        host and port. It runs the event loop until the server is terminated (e.g., via CTRL+C). 
        and handles shutdown without leaving unclean traces.
        
        Method:
            - Creates asyncio server bound to host/port.
            - Runs event loop until user exits (CTRL+C).
            - Handles graceful shutdown without traceback.
            
        Notes:
            - this server is meant for development and testing only.
        '''
        
        async def main():
            server = await asyncio.start_server(self.handle_client, self.host, self.port)
            print(f'{Fore.RED}*** This is a development server. Do not use it in production development. ***{Style.RESET_ALL}')
            self.app.logger.info(f'Citra running on {Fore.YELLOW}http://{self.host}:{self.port}{Style.RESET_ALL}')
            self.app.logger.info(f'{Fore.WHITE}Press (CTRL+C) to terminate server.{Style.RESET_ALL}')
            async with server:
                await server.serve_forever()
                
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            self.app.logger.warning(f'Citra Server stopped by user {Fore.RED}(CTRL+C){Style.RESET_ALL}')