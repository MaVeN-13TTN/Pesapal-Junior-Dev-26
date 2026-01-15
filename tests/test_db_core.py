
import pytest
import os
from src.db.table import Table, Column, ColumnType
from src.db.core import Database

def test_column_definition():
    col = Column("id", ColumnType.INTEGER, is_primary=True)
    assert col.name == "id"
    assert col.col_type == ColumnType.INTEGER
    assert col.is_primary is True

def test_table_insert_validation():
    cols = [
        Column("id", ColumnType.INTEGER, is_primary=True),
        Column("name", ColumnType.STRING)
    ]
    t = Table("users", cols)
    
    # Valid insert
    t.insert({"id": 1, "name": "Alice"})
    assert len(t.rows) == 1
    
    # Type Error
    with pytest.raises(TypeError):
        t.insert({"id": "one", "name": "Alice"})
        
    # Primary Key Violation
    with pytest.raises(ValueError):
        t.insert({"id": 1, "name": "Bob"})

def test_unique_constraint():
    cols = [
        Column("id", ColumnType.INTEGER, is_primary=True),
        Column("email", ColumnType.STRING, is_unique=True)
    ]
    t = Table("users", cols)
    
    t.insert({"id": 1, "email": "a@b.com"})
    
    # Unique Violation
    with pytest.raises(ValueError):
        t.insert({"id": 2, "email": "a@b.com"})

def test_database_persistence(tmp_path):
    db_file = tmp_path / "test_db.json"
    db = Database(str(db_file))
    
    cols = [Column("id", ColumnType.INTEGER)]
    t = Table("test", cols)
    t.insert({"id": 1})
    
    db.create_table(t)
    db.save()
    
    # Reload
    db2 = Database(str(db_file))
    db2.load()
    
    assert "test" in db2.tables
    assert len(db2.tables["test"].rows) == 1
    assert db2.tables["test"].rows[0]["id"] == 1
