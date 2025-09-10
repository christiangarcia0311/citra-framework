from citra_framework.components.response import Response

class BaseErrorPage:
    
    '''
    Base class for generating reussable, styled HTML eror pages.
    
    Provides a consistent layout for displaying HTTP error responses
    with a `status code`, `message` and `optional` details.
    
    Attributes:
        code (int): status code for the error.
        message (str): short description of the error.
        details (str, optional): additional information about the error.
        debug (bool): wether debug mode is enabled.
    '''
    
    def __init__(
        self,
        code,
        message,
        details=None,
        debug=False
    ):
        self.code = code
        self.message = message
        self.details = details
        self.debug = debug
        
    def display(self):
        
        ''' Return full HTML error page '''
        
        traceback_html = ''
        
        if self.debug and self.details:
            traceback_html = f'''
            <div class="traceback">
              <div class="title">Debug Console:</div>
              <pre>{self.details}</pre>
            </div>
            '''
            
        body = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.code} {self.message}</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    font-family: "Poppins", sans-serif;
                    background: #f3f4fb;
                    color: #333;
                }}
                
                .header {{
                    padding: 15px 30px;
                    font-size: 20px;
                    font-weight: 700;
                    color: #2563eb;
                    border-bottom: 1px solid #ddd;
                    text-shadow: 3px 3px 0 rgba(37, 99, 235, 0.3);
                }}
                
                .container {{
                    text-align: center;
                    margin-top: 60px;
                }}
                
                .error-code {{
                    font-size: 120px;
                    font-weight: 700;
                    background: linear-gradient(90deg, #f59e0b, #f97316);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin: 0;
                    text-shadow: 6px 6px 0 rgba(249, 115, 22, 0.3);
                }}
                
                .message {{
                    font-size: 22px;
                    font-weight: 500;
                    margin: 10px 0;
                }}
                
                .note {{
                    font-size: 14px;
                    color: #666;
                    max-width: 600px;
                    margin: 0 auto 40px;
                }}
                
                .note a {{
                    color: #2563eb;
                    text-decoration: none;
                    font-weight: 500;
                }}
                
                .note a:hover {{
                    text-decoration: underline;
                }}
                
                .traceback {{
                    background: #fff;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    margin: 0 auto 50px;
                    padding: 20px;
                    width: 90%;
                    max-width: 900px;
                    font-family: monospace;
                    font-size: 13px;
                    color: #111;
                    overflow-x: auto;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.05);
                }}
                
                .traceback .title {{
                    font-weight: 600;
                    margin-bottom: 10px;
                    color: #f97316;
                }}
                
                .traceback pre {{
                    margin: 0;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    line-height: 1.5;
                }}
                
                .traceback .error-line {{
                    background: #ffedd5;
                    padding: 2px 4px;
                    border-radius: 4px;
                    display: inline-block;
                }}
            
            </style>
        </head>
        <body>
        <div class="header">CITRA</div>
            <div class="container">
                <h1 class="error-code">{self.code}</h1>
                <p class="message">{self.message}</p>
                <p class="note">
                    {"You're seeing this error because your site is in <a href='#'>DEBUG</a> mode." if self.debug else "An unexpected error occurred."}
                </p>
            </div>
          {traceback_html}
        </body>
        </html>
        '''
        
        return Response(body, self.code, {'Content-Type': 'text/html'})
        
        
        
        



''' ----- Specific HTTP Errors -----'''

class InternalServerError(BaseErrorPage):
    def __init__(self, details=None, debug=False):
        
        ''' Represents an HTTP 500 Internal Server error page. '''
        
        super().__init__(500, 'Internal Server Error', details, debug)

class NotFoundError(BaseErrorPage):
    def __init__(self, details=None, debug=False):
        
        ''' Represents an HTTP 404 Not Found error page.'''
        
        super().__init__(404, 'Not Found Error', details, debug)
        
class UnauthorizedError(BaseErrorPage):
    def __init__(self, details=None, debug=False):
        
        ''' Represents an HTTP 401 Unauthorized error page. '''
        
        super().__init__(401, 'Unauthorized Access', details, debug)
