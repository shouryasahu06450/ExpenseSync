from datetime import date
from database import get_connection

def add_expense(title, amount, category, expense_date, note=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (title, amount, category, expense_date, note) VALUES (?, ?, ?, ?, ?)",
        (title, amount, category, expense_date, note)
    )
    conn.commit()
    conn.close()

def get_expenses(search="", category="", start_date="", end_date=""):
    conn = get_connection()
    sql = "SELECT * FROM expenses WHERE 1=1"
    params = []
    if search:
        sql += " AND (title LIKE ? OR note LIKE ?)"
        params += [f"%{search}%", f"%{search}%"]
    if category:
        sql += " AND category = ?"
        params.append(category)
    if start_date:
        sql += " AND expense_date >= ?"
        params.append(start_date)
    if end_date:
        sql += " AND expense_date <= ?"
        params.append(end_date)
    sql += " ORDER BY expense_date DESC, id DESC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows

def get_expense(expense_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    conn.close()
    return row

def update_expense(expense_id, title, amount, category, expense_date, note=""):
    conn = get_connection()
    conn.execute(
        """UPDATE expenses
           SET title=?, amount=?, category=?, expense_date=?, note=?
           WHERE id=?""",
        (title, amount, category, expense_date, note, expense_id)
    )
    conn.commit()
    conn.close()

def delete_expense(expense_id):
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()

def get_categories():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM categories ORDER BY name").fetchall()
    conn.close()
    return rows

def add_category(name):
    conn = get_connection()
    conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_category_totals():
    conn = get_connection()
    rows = conn.execute("""
        SELECT category, ROUND(SUM(amount), 2) AS total, COUNT(*) AS count
        FROM expenses GROUP BY category ORDER BY total DESC
    """).fetchall()
    conn.close()
    return rows

def get_dashboard_stats():
    conn = get_connection()
    total = conn.execute("SELECT COALESCE(SUM(amount),0) FROM expenses").fetchone()[0]
    month = date.today().strftime("%Y-%m")
    month_total = conn.execute(
        "SELECT COALESCE(SUM(amount),0) FROM expenses WHERE substr(expense_date,1,7)=?",
        (month,)
    ).fetchone()[0]
    count = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
    top = conn.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses GROUP BY category ORDER BY total DESC LIMIT 1
    """).fetchone()
    recent = conn.execute("""
        SELECT * FROM expenses ORDER BY expense_date DESC, id DESC LIMIT 6
    """).fetchall()
    categories = conn.execute("""
        SELECT category, ROUND(SUM(amount),2) AS total
        FROM expenses GROUP BY category ORDER BY total DESC
    """).fetchall()
    conn.close()
    return {
        "total": round(total, 2),
        "month_total": round(month_total, 2),
        "count": count,
        "top_category": top["category"] if top else "—",
        "recent": recent,
        "category_labels": [r["category"] for r in categories],
        "category_values": [r["total"] for r in categories],
    }
