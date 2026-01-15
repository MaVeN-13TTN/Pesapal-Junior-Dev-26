# Design & Implementation

## Why Python?

I chose **Python** for this challenge for several strategic reasons:

1.  **Rapid Prototyping**: Python's dynamic nature allowed me to build a working Parser, Storage Engine, and Web API in under 4 hours.
2.  **String Manipulation**: The `re` (Regex) module in Python is world-class, making it the perfect choice for implementing a custom SQL parser without needing heavy dependencies like ANTLR.
3.  **Data Structures**: Python's Dictionaries (`dict`) are highly optimized hash maps. Using them as the backbone for my In-Memory storage (`Table` rows and `Index`) ensures O(1) lookups for Primary Keys by default.
4.  **Standard Library**: Modules like `cmd` (for the REPL) and `json` (for persistence) allowed me to implement complex features with zero external dependencies for the core engine.

## Codebase Capabilities

The project is structured to enforce separation of concerns:

### Core Engine
- **`src/db/core.py`**: The "Brain". It manages the collection of tables and handles the Persistence Layer (`save`/`load` to JSON). It acts as the bridge between the Parser and the Tables.
- **`src/db/table.py`**: The "Brawn". It enforces schema constraints (Types, Primary Keys, Unique Keys). It holds the actual data in memory.

### Query Processing
- **`src/parser/parser.py`**: A custom Recursive-Descent/Regex parser. It takes raw SQL strings and converts them into structured `Command` objects (e.g., `SelectCommand`, `InsertCommand`). This decoupling means I can easily swap the syntax without breaking the execution logic.

### Interfaces
- **`src/cli.py`**: Demonstrates Python's `cmd` module to provide a robust persistence shell. It abstracts the complexity of `Database` interactions behind a simple prompt.
- **`src/app.py`**: Shows how easily the RDBMS can be embedded. Since the DB is just a Python class, Flask can import and use it directly without complex drivers or connections.
