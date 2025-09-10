import json
import urllib.parse 

class Request:
    
    '''
    HTTP Request for `Citra`
    
    Provides access to:
        - request.method -> `'GET'`, `'POST'`, etc.
        - request.path -> `'/route'`.
        - request.headers -> dictionary of headers.
        - request.json -> parsed `JSON` body.
        - request.form -> dictionary of `POST` data.
        - request.query -> dict of query parameters `(?x=1)`.
    '''   
    
    def __init__(
        self,
        method,
        path,
        headers,
        body
    ):
        
        '''
        Represent as HTTP request.
        
        Attributes:
            method (str): HTTP method `(GET, POST, etc..)`.
            path (str): request url path.
            headers (dict): HTTP headers.
            body (bytes | str): request body.
            
        '''
        
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body if isinstance(body, bytes) else body.encode()
        
        # --- parsed data ---
        self.json = None 
        self.form = {}
        self.query = self._parse_query() 
        
        if self.body and 'application/x-www-form-urlencoded' in headers.get('content-type', ''):
            parsed = urllib.parse.parse_qs(self.body.decode())
            self.form = {key: value[0] if len(value) == 1 else value for key, value in parsed.items()}
    
    def _parse_query(self):
        
        '''
        Parse query string from path
        '''  
        
        if '?' not in self.path:
            return {}
        
        query_string = self.path.split('?', 1)[1] 
        return dict(urllib.parse.parse_qsl(query_string)) 
            
    @staticmethod
    def parse(data: bytes):
        
        '''
        Parse raw HTTP data into a request object.
        
        Args:
            data (bytes): raw HTTP request data from client.
        '''
        
        text = data.decode('utf-8')
        lines =  text.split('\r\n')
        method, path, _ = lines[0].split(' ')
        headers = {}
        
        index = 1
        
        while lines[index]:
            key, value = lines[index].split(': ', 1)
            headers[key.lower()] = value
            index += 1
            
        body = '\r\n'.join(lines[index + 1:])
        return Request(method, path, headers, body)