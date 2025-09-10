from .logger import Logger
import mysql.connector as mysql

class Database:
    
    '''
    MySQL database wrapper for Citra framework.
    -------------------------------------------
    
    Attributes:
        connection: `(mysql.connector.MySQLConnection)` -> active database conenction.
        cursor: `(mysql.connector.cursor.MySQLCursor)` -> cursor for executing queries.
    '''
    
    logger = Logger('Citra::Database')
    
    def __init__(
        self,
        hostname='localhost',
        username='root',
        password='',
        database=''
    ):
        
        '''
        Initialize MySQL connection using provided config attributes.
        
        Args:
            hostname (str): database host.
            username (str): database username (root).
            password (str): database password (common is blank).
            database (str): database name.
            
        Example:
            db = Database(
                hostname='localhost',
                username='root',
                password='',
                database='citra_db'
            )
        '''
        
        # database conenction attributes.
        self.connection = None
        self.cursor = None
        
        # version 0.1.1
        try:
            self.connection = mysql.connect(
                host=hostname,
                user=username,
                password=password,
                database=database
            )
        
            self.cursor = self.connection.cursor(dictionary=True)
            self.logger.info(f'MySQL connected successfully to {database} at {hostname}')
            
        except mysql.errors.InterfaceError as e:
            self.logger.warning(f'Cannot connect to MySQL server at {hostname}:3306. Make sure the server is running. Error: {e}')
            self.connection = None
            self.cursor = None
            
        except mysql.Error as e:
            self.logger.error(f'MySQL error: {e}')
            
    # ---- Main SQL Execution function ----
    def execute(self, query, parameters=()):
        
        '''Execute a SQL query with optional parameters.'''
        
        # version 0.1.1
        if not self.cursor:
            self.logger.warning('Cannot execute query. No Database connection.')
            return None
        
        try:   
            self.cursor.execute(query, parameters)
            self.connection.commit()
            return self.cursor
        except mysql.Error as e:
            self.logger.error(f'MySQL Error: {e}')
            return None
    
    def query(self, query, parameters=()):
        
        '''Execute a SELECT query and fetchall results.'''
        
        # version 0.1.1
        if not self.cursor:
            self.logger.warning('Cannot execute query. No Database connection.')
            return []
        
        try:
            self.cursor.execute(query, parameters)
            return self.cursor.fetchall()
        except mysql.Error as e:
            self.logger.error(f'MySQL Error: {e}')
            return []
    
    # ---- Helper Functions for queries ----
    def create_table(self, table_name, **columns):
        
        '''
        Create a table in the database.
        
        Args:
            table_name (str): name of the table.
            **columns (str): column definitions.
            
        Example:
            db.create_table(
                'users',
                id='INT PRIMARY KEY',
                name='VARCHAR(50),
                age='INT'
            )
        '''
        
        # version 0.1.1
        if not self.cursor:
            self.logger.warning(f'Cannot CREATE table ({table_name}). No Database connection.')
            return 
        
        column = ', '.join([f'{var_name} {data_type}' for var_name, data_type in columns.items()])
        sql_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({column})'
        self.execute(sql_query)
        
    def insert(self, table_name, **data):
        
        '''
        Insert a data record into a table.
        
        Args:
            table_name (str): name of the table.
            **data (str): column-value pairs to insert.
            
        Example:
            db.insert(
                'users',
                id=1,
                name='Christian',
                age=22
            )
        '''
        
        # version 0.1.1
        if not self.cursor:
            self.logger.warning(f'Cannot INSERT into table ({table_name}). No Database connection.')
            return
        
        column = ', '.join(data.keys())
        placeholder = ', '.join(['%s'] * len(data))
        values = tuple(data.values())
        sql_query = f'INSERT INTO {table_name} ({column}) VALUES ({placeholder})'
        self.execute(sql_query, values)
    
    def select(self, table_name, where=None, where_values=None):
        
        '''
        Fetch data records from a table.
        
        Args:
            table_name (str): name of the table.
            where (str): sql query condition.
            
        Returns:
            list[dict]: rows as tuples retrieved from the table.
            
        Example:
            user = db.select('users')
            active_user = db.select('users', where='age > %s', age=18)
        '''
        
        # version 0.1.1
        if not self.cursor:
            self.logger.warning(f'Cannot SELECT from table ({table_name}). No Database connection.')
            return []
        
        sql_query = f'SELECT * FROM {table_name}'
        parameters = where_values or ()
        
        if where:
            sql_query += f' WHERE {where}'
            parameters = where_values or ()
        return self.query(sql_query, parameters)
    
    def update(self, table_name, where, where_values, **data):
        
        '''
        Update data records from a table.
        
        Args:
            table_name (str): name of the table.
            where (str): sql `WHERE` condition string.
            where_values (tuplr): values for the `WHERE` condition placeholders.
            **data (dict): column-value pairs to update.
        
        Example:
            db.update(
                'users',
                where='id=%s',
                where_values=(1,),
                age=25
            )
        '''
        
        # version 0.1.1
        if not self.cursor:
            self.logger.warning(f'Cannot UPDATE table ({table_name}). No Database connection.')
            return
        
        set_clause = ', '.join([f'{key}=%s' for key in data.keys()])
        sql_query = f'UPDATE {table_name} SET {set_clause} WHERE {where}'
        parameters = tuple(data.values()) + where_values
        self.execute(sql_query, parameters)
    
    def delete(self, table_name, where, where_values):
        
        '''
        Delete a data record from a table.
        
        Args:
            table_name (str): name of the table.
            where (str): sql `WHERE` condition string.
            where_values (tuple): values for the `WHERE` condtion placeholders.
        '''
        
        # version 0.1.1
        if not self.cursor:
            self.logger.warning(f'Cannot DELETE from table ({table_name}). No Database connection.')
            return
        
        sql_query = f'DELETE FROM {table_name} WHERE {where}'
        self.execute(sql_query, where_values)