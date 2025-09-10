'''
Test for database component of `Citra` framework.

Database:
    CREATE DATABASE test_db;

Table:
    CREATE TABLE citra_data(
        data_id INT AUTO_INCREMENT PRIMARY KEY, 
        data_name VARCHAR(50), 
        data_number INT 
    ); 
    

Test Development:
    PYTHONPATH=$(pwd) pytest -v tests/test_database.py
'''

from citra_framework.components.database import Database
import pytest

CONFIG_DATABASE = {
    'hostname': 'localhost',
    'username': 'root',
    'password': '',
    'database': 'test_db'
}

TABLE_NAME = 'citra_data'

@pytest.fixture(scope='module')
def database():
    database = Database(
        hostname=CONFIG_DATABASE['hostname'],
        username=CONFIG_DATABASE['username'],
        password=CONFIG_DATABASE['password'],
        database=CONFIG_DATABASE['database']
    )
    
    database.execute(f'DROP TABLE IF EXISTS {TABLE_NAME}')
    
    yield database
    
    database.execute(f'DROP TABLE IF EXISTS {TABLE_NAME}')
    
def test_connection(database):
    assert database.connection.is_connected() == True

def test_create_table(database):
    database.create_table(
        TABLE_NAME,
        data_id='INT AUTO_INCREMENT PRIMARY KEY', 
        data_name='VARCHAR(50)', 
        data_number='INT'
    )
    
    tables = database.select(
        'information_schema.tables',
        'table_schema=%s AND table_name=%s',
        (CONFIG_DATABASE["database"], TABLE_NAME)
    )
    
    assert len(tables) == 1
    
def test_insert_and_select(database):
    # --- insert sample data in table ---
    database.insert(TABLE_NAME, data_name='Citra Web Development', data_number=4570)
    database.insert(TABLE_NAME, data_name='Citra API Backend', data_number=8701)
    
    # --- select sample data in table ---
    rows = database.select(TABLE_NAME)
    data_name = [row['data_name'] for row in rows]
    data_number = [row['data_number'] for row in rows]
    
    assert 'Citra Web Development' in data_name
    assert 'Citra API Backend' in data_name
    
def test_update(database):
    database.update(TABLE_NAME, where='data_name=%s', where_values=('Citra Web Development',), data_number=9080)
    rows = database.select(TABLE_NAME, where='data_name=%s', where_values=('Citra Web Development',))
    assert rows[0]['data_number'] == 9080
    
def test_delete(database):
    database.delete(TABLE_NAME, where='data_name=%s', where_values=('Citra API Backend',))
    rows =database.select(TABLE_NAME, where='data_name=%s', where_values=('Citra API Backend',))
    assert len(rows) == 0