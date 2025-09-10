'''
Zest a lightweight template engine designed for `Citra` framework.
'''

from citra_framework.components.response import Response
import os
import re

class Zest:
    
    '''
    Zest Template Engine :: Christian Garcia | Programmer 
    --------------------
    
    Zest a lightweight HTML template engine designed for `Citra` framework.
    Allows developers to embed python-like expressions inside HTML files.
    
    Supported Features:
    -------------------
    
    1. Variable Interpolation:
        - use % variable % to insert context values.
        
        Example:
            <p>Hello, % name %</p>
        
    2. Loops:
        - use $ for item in list $ ... $ endfor $ to iterate over a list.
        
        Example:
            <ul>
                $ for item in items $
                    <li>% items %</li>
                $ endfor $
            </ul>
    
    3. Conditionals:
        - use $ if item %} ... $ endif $ to conditionally render blocks.
        
        Example:
            $ if is_active $
                <p>You are online.</p>
            $ endif $
            
    Updates:
        - v.0.1.0 -> Add Flash messages.
    '''
    
    def __init__(self, template_dir='src', router=None):
        
        '''
        Initialize the `Zest` template engine.
        
        Args:
            template_dir (str): directory containing `.html` files.
        '''
        
        self.template_dir = template_dir
        
        # router to resolve urls
        self.router = router 
        
        # temporary flash mesage
        self._flashes =[]
        
    def _load_template(self, template_name):
        
        '''
        Load raw template content from file.
        
        Args:
            template_name (str): name of the template file (e.g., 'index.html').
        '''
        
        path = os.path.join(self.template_dir, template_name)
        
        # --- Match path and read ---
        if not os.path.exists(path):
            raise FileNotFoundError(f'Template {template_name} not found.')

        with open(path, 'r', encoding='utf-8') as folder:
            return folder.read()
        
    def _process_control_structures(self, template, context):
        
        '''
        Process control structure in the template.
        
        Supports custom loop and conditional syntax and replaces them
         with rendered HTML output.
        
        Args:
            template (str): raw template string.
            context (dict): variables available to the template.
        '''
        
        # ---  Control flow structure ---
        # for Loops
        # if-else statement
        
        '''FOR LOOP SYNTAX $ for item in list $ ... $ endfor $'''
        
        for_loop_pattern = r'\$ for (\w+) in (\w+) \$(.*?)((?:\$ else \$(.*?))?)\$ endfor \$'
        def replace_forloop(match):
            var, iterable, body, _, else_body = match.groups()
            items = context.get(iterable, [])
            
            if not items:
                return else_body or ''
            
            result = ''
            
            for value in items:
                local_context = context.copy()
                local_context[var] = value
                inner = re.sub(
                    r'%\s*(.*?)\s*%',
                    lambda x: str(eval(x.group(1).strip(), {}, local_context)),
                    body
                )
                
                result += inner 
            
            return result
        
        template = re.sub(for_loop_pattern, replace_forloop, template, flags=re.S)
        
        '''IF STATEMENT SYNTAX $ if item $ ... $ endif $'''
        
        if_statement_pattern = r'\$ if (.*?) \$(.*?)((?:\$ else \$(.*?))?)\$ endif \$'
        def replace_if(match):
            condition, body, _, else_body = match.groups()
            
            try:
                if eval(condition.strip(), {}, context):
                    return body
                else:
                    return else_body or ''
            except Exception:
                return ''
        
        template = re.sub(if_statement_pattern, replace_if, template, flags=re.S)
        
        return template
    
    # --- FLASH MESSAGE ---
    def message(self, message, category='info'):
        
        '''
        Store a flash message for the next render cycle.
        
        Args:
            message (str): the messge to display.
            category (str, optional): message category (e.g., info, error, warning, success).
        '''
        
        self._flashes.append({'message': message, 'category': category})
    
    def get_flashed_message(self, clear=True):
        
        '''
        Retrieve all flash messages.
        
        Args:
            clear (bool): wether to clear messages after retrieval.
        '''
        
        messages =self._flashes.copy()
        
        if clear:
            self._flashes.clear()
        
        return messages


    '''
    display and redirect method.
    '''
    
    
    def display(
        self,
        template_name,
        context=None,
        status_code=200
    ):
        '''
        Render or display a template file into a complete `HTML` response.
        
        Args:
            template_name (str): file name of the template (must be inside `template_dir`).
            context (dict, optional): dictionary of variables passed into the template.
            status_code (int, optional): HTTP status code for the response.
        '''
        
        context = context or {}
        context['_flashes'] = self.get_flashed_message(clear=True)
        template = self._load_template(template_name)
        template = self._process_control_structures(template, context)
        
        '''VARIABLE % name %'''
        def replace_variable(match):
            expression = match.group(1).strip()
            
            try:
                return str(eval(expression, {}, context))
            except Exception:
                parts = expression.split('.')
                value = context.get(parts[0], None)
                for part in parts[1:]:
                    if isinstance(value, dict):
                        value = value.get(part, None)
                    else:
                        value = getattr(value, part, None)
                return str(value) if value is not None else f'%{expression}%'
        
        rendered = re.sub(r'%\s*(.*?)\s*%', replace_variable, template)
        
        '''ACTIONS @submit'''
        def replace_action(match):
            route_name = match.group(1).strip()
            
            if self.router:
                try:
                    self.router.url_route(route_name)
                except Exception as e:
                    return f'/{route_name}'
            return f'/{route_name}'
        
        rendered = re.sub(r'@(\w+)', replace_action, rendered)
        
        return Response(rendered, status_code, {"Content-Type": "text/html"})
    
    def forward(
        self,
        route_name,
        status_code=302,
        **kwargs
    ):
        '''
        Redirect to another route by name
        
        Args:
            route_name (str): name of the target route.
            status_code (int, optional): redirect status code.
            **kwargs: parameters for route resolution.
        '''
        
        if '_flash' in kwargs:
            self._flashes.append(kwargs['_flashes'])
            
        if self.router:
            try:
                url = self.router.url_route(route_name, **kwargs)
            except Exception:
                url = f'/{route_name}'
        else:
            url = f'/{route_name}'
            
        return Response('', status_code, headers={'Location': url})
        