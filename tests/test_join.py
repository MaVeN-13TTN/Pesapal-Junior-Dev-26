from src.db.core import Database
from src.db.table import ColumnType

def test_inner_join_execution():
    db = Database(":memory:")
    
    # Create Users
    db.execute_query("CREATE TABLE users (id INT PRIMARY KEY, name STRING)")
    db.execute_query("INSERT INTO users (id, name) VALUES (1, \"Alice\")")
    db.execute_query("INSERT INTO users (id, name) VALUES (2, \"Bob\")")
    
    # Create Orders
    db.execute_query("CREATE TABLE orders (oid INT PRIMARY KEY, user_id INT, item STRING)")
    db.execute_query("INSERT INTO orders (oid, user_id, item) VALUES (100, 1, \"Laptop\")")
    db.execute_query("INSERT INTO orders (oid, user_id, item) VALUES (101, 1, \"Mouse\")")
    db.execute_query("INSERT INTO orders (oid, user_id, item) VALUES (102, 2, \"Monitor\")")
    # Order for non-existent user? (Left join would keep it, Inner shouldn't if we had orphan check, but here simplistic)
    
    # Execute JOIN
    # SELECT * FROM users JOIN orders ON users.id = orders.user_id
    res = db.execute_query("SELECT * FROM users JOIN orders ON users.id = orders.user_id")
    
    # Expect 3 rows
    assert len(res) == 3
    
    # Verify content (merged dicts)
    # Row 1: Alice Laptop
    assert any(r['name'] == "Alice" and r['item'] == "Laptop" for r in res)
    # Row 2: Alice Mouse
    assert any(r['name'] == "Alice" and r['item'] == "Mouse" for r in res)
    # Row 3: Bob Monitor
    assert any(r['name'] == "Bob" and r['item'] == "Monitor" for r in res)

def test_join_with_where():
    db = Database(":memory:")
    db.execute_query("CREATE TABLE A (id INT, val STRING)")
    db.execute_query("CREATE TABLE B (bid INT, ref_id INT, extra STRING)")
    
    db.execute_query("INSERT INTO A (id, val) VALUES (1, \"One\")")
    db.execute_query("INSERT INTO A (id, val) VALUES (2, \"Two\")")
    
    db.execute_query("INSERT INTO B (bid, ref_id, extra) VALUES (10, 1, \"Extra1\")")
    db.execute_query("INSERT INTO B (bid, ref_id, extra) VALUES (11, 2, \"Extra2\")")
    
    # SELECT * FROM A JOIN B ON A.id = B.ref_id WHERE val="One"
    res = db.execute_query("SELECT * FROM A JOIN B ON A.id = B.ref_id WHERE val=\"One\"")
    
    assert len(res) == 1
    assert res[0]['extra'] == "Extra1"
