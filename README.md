# Pesapal Junior Dev Challenge '26 - RDBMS Solution

## Challenge Overview
Build a simple Relational Database Management System (RDBMS) with:
- Table declarations & Column types
- CRUD Operations
- Indexing & Keys (Primary/Unique)
- JOINS
- SQL-like Interface & REPL
- Demo Web App

**Deadline**: Jan 17th, 2026.

## Architecture
This solution uses **Python** for its readability and robust standard library.

- **Database Engine**: Python-based In-memory engine with JSON persistence.
- **Query Language**: Custom REGEX/Recursive-Descent parser.
- **Web Demo**: Flask web server.

## Project Structure
- `src/db/`: Core database logic.
- `src/parser/`: SQL parsing logic.
- `src/cli.py`: Interactive REPL (using `cmd` module).
- `src/app.py`: Flask web application.

## Getting Started
1. `python3 -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. `pytest` (Run checks)
4. `python src/cli.py` (Start RDBMS REPL)
5. `python src/app.py` (Start Demo Web App)
