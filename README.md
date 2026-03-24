# University QA Agent

A simple LangGraph-based QA agent for a university database.

## What it does

The system:
1. Receives a natural-language question
2. Loads database schema context
3. Generates SQL
4. Validates the SQL
5. Executes the query on SQLite
6. Returns a natural-language answer with trace information

## Requirements

- Python 3.11
- Conda
- SQLite

## Create environment

```bash
conda create -n university-qa-agent python=3.11 -y
conda activate university-qa-agent
```

## Install dependencies
```
pip install -r requirements.txt
```

## Initialize the database

### Run:
```
python scripts/init_db.py
```

This creates the SQLite database file from:

app/db/schema.sql
app/db/seed.sql

## Run the app
```
python -m app.main
```
### Example run


#### Input:

How many students are enrolled in each course?

#### Output:

Final answer:

Here's the enrollment for each course:

- Algorithms: 2 students
- Classical Mechanics: 2 students
- Databases: 5 students
- Introduction to Programming: 4 students
- Linear Algebra: 3 students


## Run tests
`pytest`

