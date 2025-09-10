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
    '''
    
    def __init__(
        self,
        code,
        message,
        details=None
    ):
        self.code = code
        self.message = message
        self.details = details
        
    def display(self):
        details_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.message}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, Helvetica, sans-serif;
            background-color: #FAC898;
        }}
        .main {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        .details {{
            text-align: justify;
            background-color: #FFEAE6;
            color: #4e4d4d;
            width: 500px;
        }}
        h1 {{
            color: #ff4019;
        }}
        p {{
            padding: 10px 10px;
        }}
    </style>
</head>
<body>
    <div class="main">
        <div class="inner">
            <h1>{self.code} {self.message}</h1>
            <div class="details">
                <p>{self.details}</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
        return Response(details_html, status_code=self.code, headers={'Content-Type': 'text/html'})



''' ----- Specific HTTP Errors -----'''

class InternalServerError(BaseErrorPage):
    def __init__(self, details=None):
        
        ''' Represents an HTTP 500 Internal Server error page. '''
        
        super().__init__(500, 'Internal Server Error', details)

class NotFoundError(BaseErrorPage):
    def __init__(self, details=None):
        
        ''' Represents an HTTP 404 Not Found error page.'''
        
        super().__init__(404, 'Not Found Error', details)
        
class UnauthorizedError(BaseErrorPage):
    def __init__(self, details=None):
        
        ''' Represents an HTTP 401 Unauthorized error page. '''
        super().__init__(401, 'Unauthorized Access', details)
