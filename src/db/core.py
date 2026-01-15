import json
import os
from typing import Dict, Optional
from .table import Table

class Database:
    def __init__(self, persistence_file: str = "db.json"):
        self.tables: Dict[str, Table] = {}
        self.persistence_file = persistence_file

    def create_table(self, table: Table) -> None:
        if table.name in self.tables:
            raise ValueError(f"Table '{table.name}' already exists.")
        self.tables[table.name] = table

    def get_table(self, name: str) -> Optional[Table]:
        return self.tables.get(name)

    def drop_table(self, name: str) -> None:
        if name in self.tables:
            del self.tables[name]

    def save(self) -> None:
        """Persist all tables to disk."""
        data = {
            "tables": {name: table.to_dict() for name, table in self.tables.items()}
        }
        with open(self.persistence_file, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self) -> None:
        """Load tables from disk."""
        if not os.path.exists(self.persistence_file):
            return
        
        try:
            with open(self.persistence_file, 'r') as f:
                data = json.load(f)
                for name, table_data in data.get("tables", {}).items():
                    self.tables[name] = Table.from_dict(table_data)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Failed to load database: {e}")
