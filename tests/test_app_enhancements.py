import pytest
from src.app import app
from src.db.core import Database

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_tables_empty(client):
    """Test fetching tables when database is empty."""
    # Reset DB for test
    from src.app import db
    db.tables = {} 
    
    rv = client.get('/api/tables')
    assert rv.status_code == 200
    assert rv.json == {}

def test_api_query_metadata(client):
    """Test that query response includes metadata."""
    rv = client.post('/api/query', json={'query': 'CREATE TABLE test_meta (id INT)'})
    assert rv.status_code == 200
    data = rv.json
    assert "meta" in data
    assert "duration_seconds" in data["meta"]
    assert "status" in data["meta"]
    assert data["meta"]["status"] == "200 OK"

def test_get_tables_populated(client):
    """Test fetching tables after creation."""
    client.post('/api/query', json={'query': 'CREATE TABLE users (id INT, name STRING)'})
    
    rv = client.get('/api/tables')
    assert rv.status_code == 200
    tables = rv.json
    assert "users" in tables
    assert len(tables["users"]["columns"]) == 2
    assert tables["users"]["columns"][0]["name"] == "id"
