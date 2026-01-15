
import pytest
from src.db.core import Database

@pytest.fixture
def db():
    return Database(":memory:")

def test_sql_create_insert_select(db):
    db.execute_query("CREATE TABLE users (id INT PRIMARY KEY, name TEXT)")
    
    assert "users" in db.tables
    
    res = db.execute_query("INSERT INTO users (id, name) VALUES (1, 'Alice')")
    assert res == "Row inserted."
    
    rows = db.execute_query("SELECT * FROM users")
    assert len(rows) == 1
    assert rows[0]['name'] == 'Alice'

def test_sql_where_clause(db):
    db.execute_query("CREATE TABLE items (id INT, type TEXT)")
    db.execute_query("INSERT INTO items (id, type) VALUES (1, 'A')")
    db.execute_query("INSERT INTO items (id, type) VALUES (2, 'B')")
    
    rows = db.execute_query("SELECT * FROM items WHERE type='B'")
    assert len(rows) == 1
    assert rows[0]['id'] == 2

def test_sql_update_delete(db):
    db.execute_query("CREATE TABLE data (id INT, val INT)")
    db.execute_query("INSERT INTO data (id, val) VALUES (1, 10)")
    
    db.execute_query("UPDATE data SET val=20 WHERE id=1")
    rows = db.execute_query("SELECT * FROM data")
    assert rows[0]['val'] == 20
    
    db.execute_query("DELETE FROM data WHERE id=1")
    rows = db.execute_query("SELECT * FROM data")
    assert len(rows) == 0
