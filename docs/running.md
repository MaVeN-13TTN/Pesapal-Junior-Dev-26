# Running the Project

## Prerequisites
- **Python 3.10+** (Required for match/case and type hinting features)
- **pip** (Python package manager)

## Installation

1. **Clone the repository**:
   ```bash
   git clone git@github.com:MaVeN-13TTN/Pesapal-Junior-Dev-26.git
   cd Pesapal-Junior-Dev-26
   ```

2. **Set up Virtual Environment**:
   It is recommended to run this project in an isolated environment.
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Modes

This RDBMS comes with three distinct ways to interact with it:

### 1. Interactive REPL (Command Line)
Directly interact with the database engine using SQL commands. This mode persists data to `db.json` upon exit.

```bash
python src/cli.py
```

**Commands**:
- `CREATE TABLE <name> (<columns>)`: Define a new table.
- `INSERT INTO <name> ...`: Add data.
- `SELECT * FROM <name>`: Query data.
  - Supports `WHERE` clauses (e.g., `WHERE id=1`).
- `exit` or `quit`: Save to disk and close the REPL.

### 2. Web Application Demo
A browser-based interface to demonstrate the RDBMS in a real-world context (via a Flask API).

```bash
python src/app.py
```

- Open your browser to **[http://localhost:3000](http://localhost:3000)**.
- The UI allows you to type raw SQL queries and visualize the results in a formatted table.

### 3. Automated Tests
Run the test suite to verify the integrity of the storage engine and SQL parser.

```bash
pytest
```
