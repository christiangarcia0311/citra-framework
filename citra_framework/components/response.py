import json 

class Response:
    
    '''
    Represents an HTTP response for `Citra` framework.
    '''
    
    def __init__(
        self,
        body='',
        status_code=200,
        headers=None
    ):
        
        '''
        HTTP response.
        
        Attributes:
            body (str | bytes): response body.
            status_code (int): HTTP status code defaults to `200`.
            headers (dict): response headers.
        '''
        self.body = body
        self.status_code = status_code
        self.headers = headers or {}
    
    def build(self):
        
        '''
        For building final HTTP response as bytes.
        '''
        
        
        # --- Detects if the content is string bytes or dictionary. ---
        if isinstance(self.body, dict):
            body_bytes = json.dumps(self.body).encode()
            self.headers.setdefault("Content-Type", "application/json")
        elif isinstance(self.body, str):
            body_bytes = self.body.encode()
            self.headers.setdefault("Content-Type", "text/html")
        elif isinstance(self.body, (bytes, bytearray)):
            body_bytes = self.body
        elif self.body is None:
            body_bytes = b''
        else:
            body_bytes = self.body
        
        headers = ''.join(f'{key}: {value}\r\n' for key, value in self.headers.items())
        
        response = (
            f'HTTP/1.1 {self.status_code} OK\r\n'
            f'Content-Length: {len(body_bytes)}\r\n'
            f'{headers}\r\n'
        ).encode() + body_bytes
        
        return response
    
    # --- Optional JSON format text ---
    @staticmethod
    def Json(data, status_code=200):
        
        '''
        Returning a json-formatted response.
        
        Args:
            data (dict): data to serialize as JSON.
            status_code (int, optional): HTTP status code defaults to `200`.
        '''
        
        content = json.dumps(data)
        return Response(content, status_code, {'Content-Type': 'application/json'})