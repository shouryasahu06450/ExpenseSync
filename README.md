# ExpenseSync — Web Expense Tracker

ExpenseSync is a Python web-based expense tracker rebuilt from the original Ledger desktop concept.

## Stack
- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Chart.js

## Features
- Dashboard with total spending and monthly spending
- Category-wise spending chart
- Recent transactions
- Add, edit and delete expenses
- Search expenses
- Category filtering
- Date-range filtering
- Category management
- SQLite persistent storage

## Project structure
```text
ExpenseSync/
├── app.py
├── database.py
├── crud.py
├── requirements.txt
├── templates/
├── static/
└── database/
```

## Run locally

### 1. Create virtual environment
```bash
python -m venv venv
```

### 2. Activate it on Windows
```bash
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the server
```bash
python app.py
```

### 5. Open in browser
Go to:
`http://127.0.0.1:5000`

The SQLite database is created automatically on first run.
