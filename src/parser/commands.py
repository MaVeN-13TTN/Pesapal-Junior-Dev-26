from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from src.db.table import ColumnType

@dataclass
class CreateTableCommand:
    table_name: str
    columns: List[Dict[str, Any]] # format: {name, type, is_primary, is_unique}

@dataclass
class InsertCommand:
    table_name: str
    values: Dict[str, Any]

@dataclass
class SelectCommand:
    table_name: str
    columns: List[str] # "*" or specific columns
    where: Optional[Dict[str, Any]] = None
    join: Optional[Dict[str, str]] = None # format: {table: "other_table", on_col: "col", target_col: "target_col"}


@dataclass
class UpdateCommand:
    table_name: str
    updates: Dict[str, Any]
    where: Optional[Dict[str, Any]] = None

@dataclass
class DeleteCommand:
    table_name: str
    where: Optional[Dict[str, Any]] = None
