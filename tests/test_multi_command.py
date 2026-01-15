import pytest
from src.db.core import Database

def test_multi_statement_insert():
    # Setup
    db = Database(":memory:") # Use string to imply ephemeral or mock, though our DB class takes file path.
    # We'll use a temp file logic or just let it use default if it wasn't persistent? 
    # The class init `Database(persistence_file="db.json")`
    # Let's use a temporary file for safety
    import os
    test_db_file = "test_multi.json"
    if os.path.exists(test_db_file):
        os.remove(test_db_file)
        
    db = Database(test_db_file)
    
    # 1. Create Table
    db.execute_query("CREATE TABLE users (id INT PRIMARY KEY, name STRING, age INT);")
    
    # 2. Multi-line Insert
    sql = """
    INSERT INTO users (id, name, age) VALUES (1, 'Alice', 30);
    INSERT INTO users (id, name, age) VALUES (2, 'Bob', 25);
    """
    results = db.execute_query(sql)
    
    # Verify results logic (it might return a list of "Row inserted.")
    assert isinstance(results, list)
    assert len(results) == 2
    assert results[0] == "Row inserted."
    assert results[1] == "Row inserted."
    
    # 3. Verify Data
    rows = db.execute_query("SELECT * FROM users")
    assert len(rows) == 2
    ids = sorted([r['id'] for r in rows])
    assert ids == [1, 2]

    # Cleanup
    if os.path.exists(test_db_file):
        os.remove(test_db_file)
