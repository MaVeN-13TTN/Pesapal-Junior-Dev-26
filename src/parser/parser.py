import re
from typing import Any, Union, Dict
from src.db.table import ColumnType
from .commands import (
    CreateTableCommand, InsertCommand, SelectCommand, 
    UpdateCommand, DeleteCommand
)

class SQLParser:
    def parse(self, query: str) -> Any:
        query = query.strip()
        if not query:
            raise ValueError("Empty query")

        # Simple regex patterns for our supported subset
        # CREATE TABLE table_name (col1 type constraint, ...)
        if re.match(r'^CREATE TABLE', query, re.IGNORECASE):
            return self._parse_create(query)
        
        # INSERT INTO table_name (col1, col2) VALUES (val1, val2)
        elif re.match(r'^INSERT INTO', query, re.IGNORECASE):
            return self._parse_insert(query)

        # SELECT * FROM table_name [WHERE col=val]
        elif re.match(r'^SELECT', query, re.IGNORECASE):
            return self._parse_select(query)
            
        # UPDATE table_name SET col=val [WHERE col=val]
        elif re.match(r'^UPDATE', query, re.IGNORECASE):
            return self._parse_update(query)
        
        # DELETE FROM table_name [WHERE col=val]
        elif re.match(r'^DELETE FROM', query, re.IGNORECASE):
            return self._parse_delete(query)

        else:
            raise ValueError("Unsupported SQL command or syntax error")

    def _parse_create(self, query: str) -> CreateTableCommand:
        # Regex to capture table name and columns part
        match = re.search(r'CREATE TABLE\s+(\w+)\s*\((.+)\)', query, re.IGNORECASE | re.DOTALL)
        if not match:
            raise ValueError("Invalid CREATE TABLE syntax")
        
        table_name = match.group(1)
        columns_str = match.group(2)
        columns = []
        
        # Split columns by comma
        col_defs = [c.strip() for c in columns_str.split(',')]
        for col_def in col_defs:
            parts = col_def.split()
            name = parts[0]
            col_type_str = parts[1].upper()
            
            # Map SQL types to Enum
            type_map = {
                "INT": ColumnType.INTEGER,
                "INTEGER": ColumnType.INTEGER,
                "TEXT": ColumnType.STRING,
                "STRING": ColumnType.STRING,
                "FLOAT": ColumnType.FLOAT,
                "BOOL": ColumnType.BOOLEAN
            }
            if col_type_str not in type_map:
                raise ValueError(f"Unknown type: {col_type_str}")
            
            is_primary = "PRIMARY KEY" in col_def.upper()
            is_unique = "UNIQUE" in col_def.upper()
            
            columns.append({
                "name": name,
                "type": type_map[col_type_str],
                "is_primary": is_primary,
                "is_unique": is_unique
            })
            
        return CreateTableCommand(table_name, columns)

    def _parse_insert(self, query: str) -> InsertCommand:
        match = re.search(r'INSERT INTO\s+(\w+)\s*\((.+?)\)\s*VALUES\s*\((.+?)\)', query, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid INSERT syntax")
            
        table_name = match.group(1)
        cols = [c.strip() for c in match.group(2).split(',')]
        vals_str = match.group(3)
        
        # Rudimentary value splitting (doesn't handle commas inside quotes well, but sufficient for basic demo)
        vals = [v.strip().strip("'\"") for v in vals_str.split(',')]
        
        if len(cols) != len(vals):
            raise ValueError("Column count doesn't match value count")
            
        # Try to infer number types
        parsed_vals = {}
        for c, v in zip(cols, vals):
            if v.isdigit():
                parsed_vals[c] = int(v)
            elif v.lower() == 'true':
                parsed_vals[c] = True
            elif v.lower() == 'false':
                parsed_vals[c] = False
            else:
                try: 
                     parsed_vals[c] = float(v)
                except ValueError:
                     parsed_vals[c] = v # keep as string
                     
        return InsertCommand(table_name, parsed_vals)

    def _parse_select(self, query: str) -> SelectCommand:
        # Improved regex to handle JOINs
        # Pattern: SELECT cols FROM table [JOIN join_table ON cond] [WHERE cond]
        
        # Regex explanation:
        # SELECT\s+(.+?)\s+FROM\s+(\w+)   -> Basic SELECT
        # (?:\s+JOIN\s+(\w+)\s+ON\s+(.+?))? -> Optional JOIN group (table and condition)
        # (?:\s+WHERE\s+(.+))?            -> Optional WHERE group (greedy match to end, might need refining if we have more clauses)
        
        match = re.search(r'SELECT\s+(.+?)\s+FROM\s+(\w+)(?:\s+JOIN\s+(\w+)\s+ON\s+(.+?))?(?:\s+WHERE\s+(.+))?$', query, re.IGNORECASE)
        if not match:
            # Fallback for simple SELECT if complex one fails (regexes can be finicky)
            match = re.search(r'SELECT\s+(.+?)\s+FROM\s+(\w+)(?:\s+WHERE\s+(.+))?', query, re.IGNORECASE)
            if not match:
                raise ValueError("Invalid SELECT syntax")
                
            # If fallback matched, checking groups carefully
            cols_str = match.group(1)
            table_name = match.group(2)
            join_table = None
            join_condition = None
            where_clause = match.group(3)
        else:
            cols_str = match.group(1)
            table_name = match.group(2)
            join_table = match.group(3)
            join_condition = match.group(4)
            where_clause = match.group(5)
        
        columns = [c.strip() for c in cols_str.split(',')]
        
        join_data = None
        if join_table and join_condition:
            # Parse JOIN condition: t1.col = t2.col
            # Simple assumption: col1 = col2
            j_match = re.search(r'(\w+\.\w+|\w+)\s*=\s*(\w+\.\w+|\w+)', join_condition)
            if j_match:
                left = j_match.group(1).split('.')[-1] # take col name only
                right = j_match.group(2).split('.')[-1]
                join_data = {
                    "table": join_table,
                    "left_col": left,
                    "right_col": right
                }
        
        where = self._parse_where(where_clause) if where_clause else None
        
        return SelectCommand(table_name, columns, where, join_data)
        
    def _parse_where(self, where_str: str) -> Dict[str, Any]:
        # Very simple WHERE parser: col = val
        match = re.search(r'(\w+)\s*=\s*(.+)', where_str)
        if not match:
            return {}
        key = match.group(1)
        val = match.group(2).strip().strip("'\"")
        
        if val.isdigit(): val = int(val)
        return {key: val}

    def _parse_update(self, query: str) -> UpdateCommand:
        # UPDATE table SET col=val WHERE ...
        match = re.search(r'UPDATE\s+(\w+)\s+SET\s+(.+?)(?:\s+WHERE\s+(.+))?$', query, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid UPDATE syntax")
            
        table_name = match.group(1)
        set_clause = match.group(2)
        where_clause = match.group(3)
        
        updates = self._parse_where(set_clause) # reuse where parser logic as it's just k=v
        where = self._parse_where(where_clause) if where_clause else None
        
        return UpdateCommand(table_name, updates, where)

    def _parse_delete(self, query: str) -> DeleteCommand:
        match = re.search(r'DELETE FROM\s+(\w+)(?:\s+WHERE\s+(.+))?', query, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid DELETE syntax")
            
        table_name = match.group(1)
        where_clause = match.group(2)
        where = self._parse_where(where_clause) if where_clause else None
        
        return DeleteCommand(table_name, where)
