from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db
from crud import (
    get_dashboard_stats, get_expenses, get_expense, add_expense,
    update_expense, delete_expense, get_categories, add_category,
    get_category_totals
)

app = Flask(__name__)
app.secret_key = "expensesync-dev-key"
init_db()

@app.route("/")
def dashboard():
    stats = get_dashboard_stats()
    return render_template("dashboard.html", stats=stats)

@app.route("/expenses")
def expenses():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    start_date = request.args.get("start_date", "").strip()
    end_date = request.args.get("end_date", "").strip()
    rows = get_expenses(search, category, start_date, end_date)
    categories = get_categories()
    return render_template(
        "expenses.html", expenses=rows, categories=categories,
        search=search, selected_category=category,
        start_date=start_date, end_date=end_date
    )

@app.route("/expenses/add", methods=["GET", "POST"])
def add():
    categories = get_categories()
    if request.method == "POST":
        try:
            title = request.form["title"].strip()
            amount = float(request.form["amount"])
            category = request.form["category"].strip()
            date = request.form["date"]
            note = request.form.get("note", "").strip()
            if not title or amount <= 0 or not category or not date:
                raise ValueError("Please enter valid expense details.")
            add_expense(title, amount, category, date, note)
            flash("Expense added successfully.", "success")
            return redirect(url_for("expenses"))
        except (ValueError, TypeError):
            flash("Please enter valid expense details.", "error")
    return render_template("expense_form.html", expense=None, categories=categories)

@app.route("/expenses/<int:expense_id>/edit", methods=["GET", "POST"])
def edit(expense_id):
    expense = get_expense(expense_id)
    if not expense:
        flash("Expense not found.", "error")
        return redirect(url_for("expenses"))
    categories = get_categories()
    if request.method == "POST":
        try:
            title = request.form["title"].strip()
            amount = float(request.form["amount"])
            category = request.form["category"].strip()
            date = request.form["date"]
            note = request.form.get("note", "").strip()
            if not title or amount <= 0 or not category or not date:
                raise ValueError
            update_expense(expense_id, title, amount, category, date, note)
            flash("Expense updated successfully.", "success")
            return redirect(url_for("expenses"))
        except (ValueError, TypeError):
            flash("Please enter valid expense details.", "error")
    return render_template("expense_form.html", expense=expense, categories=categories)

@app.post("/expenses/<int:expense_id>/delete")
def delete(expense_id):
    delete_expense(expense_id)
    flash("Expense deleted.", "success")
    return redirect(url_for("expenses"))

@app.route("/categories", methods=["GET", "POST"])
def categories():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            try:
                add_category(name)
                flash("Category added.", "success")
            except Exception:
                flash("Category already exists.", "error")
        else:
            flash("Category name is required.", "error")
        return redirect(url_for("categories"))
    return render_template("categories.html", categories=get_categories(), totals=get_category_totals())

if __name__ == "__main__":
    app.run(debug=True)
