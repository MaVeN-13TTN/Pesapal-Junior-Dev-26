# Pesapal Junior Dev Challenge '26 - RDBMS Solution

A custom-built Relational Database Management System (RDBMS) implemented in Python.

## Quick Links
- **[Setup & Running](docs/running.md)**: Instructions on how to install and run the project (REPL & Web App).
- **[Architecture](docs/architecture.md)**: High-level system overview and diagrams.
- **[Documentation](docs/documentation.md)**: Design choices, capabilities, and "Why Python?".

## Challenge Overview
**Goal**: Design and implement a simple RDBMS with support for:
- Table declarations & Data types (Integer, String, Float, Boolean)
- CRUD Operations (Create, Read, Update, Delete)
- Indexing (Primary & Unique Keys)
- Interactive SQL Shell (REPL)
- Demo Web Application

**Deadline**: Jan 17th, 2026.

## One-Line Start
```bash
# Clone, Install, and Run REPL
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python src/cli.py
```

## Project Structure
```
.
├── src/
│   ├── db/          # Core Storage Engine & Table Logic
│   ├── parser/      # Custom SQL Parser (Regex-based)
│   ├── cli.py       # Interactive Command Line Interface
│   └── app.py       # Flask Web Application Demo
├── docs/            # Detailed Documentation
├── tests/           # Automated Test Suite
└── db.json          # Persistent Storage File
```
