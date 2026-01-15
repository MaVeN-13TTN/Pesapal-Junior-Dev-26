from enum import Enum
from typing import Any, Dict, List, Optional, Union

class ColumnType(Enum):
    INTEGER = "INTEGER"
    STRING = "STRING"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"

class Column:
    def __init__(self, name: str, col_type: ColumnType, is_primary: bool = False, is_unique: bool = False, nullable: bool = True):
        self.name = name
        self.col_type = col_type
        self.is_primary = is_primary
        self.is_unique = is_unique
        self.nullable = nullable

class Table:
    def __init__(self, name: str, columns: List[Column]):
        self.name = name
        self.columns = {col.name: col for col in columns}
        self.rows: List[Dict[str, Any]] = []
        # Basic indexing for primary/unique keys
        self._primary_key_index: Dict[Any, int] = {} # maps key value to row index
        self._unique_indices: Dict[str, Dict[Any, int]] = {} # maps col_name -> {value -> row_index}
        
        # Initialize unique indices
        for col in columns:
            if col.is_unique and not col.is_primary:
                self._unique_indices[col.name] = {}

    def insert(self, row_data: Dict[str, Any]) -> None:
        # Validate schema
        validated_row = {}
        
        for col_name, col_def in self.columns.items():
            val = row_data.get(col_name)

            if val is None:
                if not col_def.nullable and not col_def.is_primary: # Auto-increment logic typically separate, but for now simple check
                     raise ValueError(f"Column '{col_name}' cannot be null")
                validated_row[col_name] = None
                continue
            
            # Type checking (simple)
            if col_def.col_type == ColumnType.INTEGER and not isinstance(val, int):
                raise TypeError(f"Column '{col_name}' expected INTEGER, got {type(val)}")
            elif col_def.col_type == ColumnType.STRING and not isinstance(val, str):
                raise TypeError(f"Column '{col_name}' expected STRING, got {type(val)}")
            
            # Unique/Primary checks
            if col_def.is_primary:
                if val in self._primary_key_index:
                    raise ValueError(f"Duplicate primary key '{val}' for column '{col_name}'")
                self._primary_key_index[val] = len(self.rows)
            
            if col_def.is_unique and not col_def.is_primary:
                 if val in self._unique_indices[col_name]:
                     raise ValueError(f"Duplicate unique value '{val}' for column '{col_name}'")
                 self._unique_indices[col_name][val] = len(self.rows)

            validated_row[col_name] = val

        self.rows.append(validated_row)

    def select(self, where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        # O(N) scan for now, optimizing later
        if not where:
            return self.rows
        
        results = []
        for row in self.rows:
            match = True
            for k, v in where.items():
                if row.get(k) != v:
                    match = False
                    break
            if match:
                results.append(row)
        return results

    def to_dict(self) -> Dict[str, Any]:
        """Serialize table to dict for persistence."""
        return {
            "name": self.name,
            "columns": [
                {
                    "name": c.name,
                    "type": c.col_type.value,
                    "is_primary": c.is_primary,
                    "is_unique": c.is_unique,
                    "nullable": c.nullable
                } 
                for c in self.columns.values()
            ],
            "rows": self.rows
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Table':
        cols = [
            Column(
                c["name"], 
                ColumnType(c["type"]), 
                c["is_primary"], 
                c["is_unique"],
                c.get("nullable", True)
            ) 
            for c in data["columns"]
        ]
        table = Table(data["name"], cols)
        table.rows = data["rows"]
        # Rebuild index
        for idx, row in enumerate(table.rows):
            for col in cols:
                val = row.get(col.name)
                if val is None: continue
                
                if col.is_primary:
                     table._primary_key_index[val] = idx
                if col.is_unique and not col.is_primary:
                    if col.name not in table._unique_indices:
                        table._unique_indices[col.name] = {}
                    table._unique_indices[col.name][val] = idx
        return table
