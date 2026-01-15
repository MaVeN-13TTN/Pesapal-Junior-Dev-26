import pytest
from src.parser.parser import SQLParser
from src.parser.commands import SelectCommand, InsertCommand, CreateTableCommand

def test_select_with_semicolon():
    parser = SQLParser()
    query = "SELECT * FROM users;"
    command = parser.parse(query)
    assert isinstance(command, SelectCommand)
    assert command.table_name == "users"

def test_select_without_semicolon():
    parser = SQLParser()
    query = "SELECT * FROM users"
    command = parser.parse(query)
    assert isinstance(command, SelectCommand)
    assert command.table_name == "users"

def test_insert_with_semicolon():
    parser = SQLParser()
    query = "INSERT INTO users (id, name) VALUES (1, 'Test');"
    command = parser.parse(query)
    assert isinstance(command, InsertCommand)
    assert command.table_name == "users"
    assert command.values == {'id': 1, 'name': 'Test'}

def test_create_with_semicolon():
    parser = SQLParser()
    query = "CREATE TABLE test (id INT);"
    command = parser.parse(query)
    assert isinstance(command, CreateTableCommand)
    assert command.table_name == "test"

def test_multiple_semicolons_trailing():
    # While not strictly required, stripping logic often handles this. 
    # Let's see if our implementation `rstrip(';')` handles `;;`
    parser = SQLParser()
    query = "SELECT * FROM users;;"
    command = parser.parse(query)
    assert isinstance(command, SelectCommand)
