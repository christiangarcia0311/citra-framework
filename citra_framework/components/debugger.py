from .error_pages.error import InternalServerError
# from .response import Response 
import traceback

class Debugger:
    
    '''
    Handles exception reporting for `Citra` framework.
    Provides different behaviors depending on wether debug mode is enabled.
    
    Attributes:
        enabled (bool): flag to enable or disable debug mode.
        logger (Logger): logger instance for logging errors.
    '''
    
    def __init__(self, enabled=False, logger=None):
        
        '''
        Initialize the debugger.
        
        Args:
            enabled (bool, optional): wether switch to enable and disable. defaults to `False`.
            logger (Logger, optional): logger instance for logging errors.
        '''
        
        self.enabled = enabled
        self.logger = logger 
        
    def handle_exception(self, e):
        
        '''
        Handle exceptions raised during request processing.
        
        Args:
            e (Exception): the exception that was raised.
        '''
        
        if self.enabled:
            tracebacks = traceback.format_exc()
            
            if self.logger:
                self.logger.error(f'Debug Exception:\n{tracebacks}')
            
            return InternalServerError(details=tracebacks).display()
            
            # --- Previous solution ---
            # error_body = f'<h1>500 Internal Server Error</h1><pre>{tracebacks}</pre>'
            # return Response(error_body, 500, {"Content-Type": "text/html"})

        else:
            if self.logger:
                self.logger.error(f'Server error: {e}')
        
        # --- Previous solution ---
        
            #error_page = InternalServerError().display()
            #error_body = f'<h1>500 Internal Server Error</h1>'
            #return Response(error_body, 500, {"Content-Type": "text/html"})
            #return Response(error_page, 500, {'Content-Tyoe': 'text/html'})
        
            return InternalServerError(details=f'Something wrong on our side. Please try again later.').display()
