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

#### Sample Workflow
Try these commands in order to verify functionality:

1. **Create a Table**:
   ```sql
   CREATE TABLE users (id INT PRIMARY KEY, name STRING, age INT)
   ```

2. **Insert Data**:
   ```sql
   INSERT INTO users (id, name, age) VALUES (1, "Alice", 30)
   INSERT INTO users (id, name, age) VALUES (2, "Bob", 25)
   ```

3. **Select Data**:
   ```sql
   SELECT * FROM users
   SELECT name FROM users WHERE age=30
   ```

4. **Update Data**:
   ```sql
   UPDATE users SET age=31 WHERE name="Alice"
   ```

5. **Delete Data**:
   ```sql
   DELETE FROM users WHERE id=2
   ```

6. **Join Data**:
   ```sql
   CREATE TABLE orders (oid INT, user_id INT, amount FLOAT)
   INSERT INTO orders (oid, user_id, amount) VALUES (100, 1, 50.5)
   SELECT * FROM users JOIN orders ON users.id = orders.user_id
   ```

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

## Data Persistence & Resetting

The database state is persisted to a file named `db.json` in the project root directory.

- **Persistence**: Data is saved automatically when you exit the REPL or modify data via the Web App.
- **Resetting**: To clear all data and start fresh, simply delete the `db.json` file:
  ```bash
  rm db.json
  ```
  The system will automatically create a new, empty database file on the next run.
