from colorama import Fore, Back, Style
import datetime
import sys

class Logger:
    
    '''
    Customize logger for tracking logs.
    
    Attributes:
        app_name (str, optional): identifier to prefix logs `(default to 'Citra')`.

    '''
    
    LEVELS = {
        'DEBUG': f'{Fore.BLUE}[DEBUG]{Style.RESET_ALL}',
        'INFO': f'{Fore.GREEN}[INFO]{Style.RESET_ALL}',
        'WARNING': f'{Fore.YELLOW}[WARNING]{Style.RESET_ALL}',
        'ERROR': f'{Fore.RED}[ERROR]{Style.RESET_ALL}'
    }
    
    def __init__(self, app_name='Citra'):
        
        ''' Customize app name for logger. '''
        
        self.app_name = app_name 
        
    def _log(self, level, message):
        
        '''
        Private helper to format and print log message.
        
        Args: 
            level (str): log severity (INFO, DEBUG, ERROR, etc..).
            message (str): message to log.
        '''
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted = f'{Fore.MAGENTA}[{timestamp}]{Style.RESET_ALL} {self.LEVELS.get(level, '[LOG]')} {self.app_name}: {message}'
        print(formatted, file=sys.stderr if level == 'ERROR' else sys.stdout)
    
    # ---- Log levels ----
    # > DEBUG Level
    # > INFO Level
    # > WARNING Level
    # > ERROR Level
    def debug(self, message):
        
        '''
        Log an DEBUG level message.

        Args:
            message (str): log content.
        '''
        
        self._log('DEBUG', message)
        
    def info(self, message):
        
        '''
        Log an INFO level message.

        Args:
            message (str): log content.
        '''
        
        self._log('INFO', message)
    
    def warning(self, message):
        
        '''
        Log an WARNING level message.

        Args:
            message (str): log content.
        '''
        
        self._log('WARNING', message)
    
    def error(self, message):
        
        '''
        Log an ERROR level message.

        Args:
            message (str): log content.
        '''
        
        self._log('ERROR', message)
    
    