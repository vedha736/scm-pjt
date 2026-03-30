# /src/backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import hashlib
import datetime

app = Flask(__name__)
CORS(app)

# ----- DB Connection -----
def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="smart_expense_tracker",
        cursorclass=pymysql.cursors.DictCursor
    )

# ----- ROUTES -----

# Register User
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    hashed_pw = hashlib.sha256(data['password'].encode()).hexdigest()
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (data['username'], data['email'], hashed_pw)
        )
        db.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Login User
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    hashed_pw = hashlib.sha256(data['password'].encode()).hexdigest()
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (data['email'], hashed_pw)
    )
    user = cursor.fetchone()
    if user:
        return jsonify({"message": "Login successful", "user_id": user['id']}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Add Expense
@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """INSERT INTO expenses (user_id, category_id, title, amount, date, description, payment_mode)
           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (data['user_id'], data['category_id'], data['title'],
         data['amount'], data['date'], data['description'], data['payment_mode'])
    )
    db.commit()
    return jsonify({"message": "Expense added!"}), 201

# Get All Expenses
@app.route('/api/expenses/<int:user_id>', methods=['GET'])
def get_expenses(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """SELECT e.*, c.name as category_name, c.icon
           FROM expenses e LEFT JOIN categories c ON e.category_id = c.id
           WHERE e.user_id = %s ORDER BY e.date DESC""",
        (user_id,)
    )
    expenses = cursor.fetchall()
    return jsonify(expenses), 200

# Get Summary
@app.route('/api/summary/<int:user_id>', methods=['GET'])
def get_summary(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT SUM(amount) as total FROM expenses WHERE user_id=%s", (user_id,)
    )
    total = cursor.fetchone()
    cursor.execute(
        """SELECT c.name, SUM(e.amount) as spent
           FROM expenses e JOIN categories c ON e.category_id = c.id
           WHERE e.user_id=%s GROUP BY c.name""",
        (user_id,)
    )
    by_category = cursor.fetchall()
    return jsonify({"total": total, "by_category": by_category}), 200

# Delete Expense
@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=%s", (expense_id,))
    db.commit()
    return jsonify({"message": "Deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
