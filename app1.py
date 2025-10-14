import os
import numpy as np
import sympy as sp
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, login_required, logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# -------------------------------------------------------------------
# Environment Setup
# -------------------------------------------------------------------
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "replace_this_with_a_secure_random_string")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///calculator.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------------------------------------------------------
# Login Manager
# -------------------------------------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# -------------------------------------------------------------------
# User Model
# -------------------------------------------------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("calculator"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return redirect(url_for("register"))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("calculator"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

# -------------------------------------------------------------------
# Calculator Logic
# -------------------------------------------------------------------
def safe_evaluate(expression):
    """
    Safely evaluate mathematical expressions with sympy.
    Supports trig, inverse trig, log, exp, matrix operations.
    """
    try:
        # Matrix input example: [[1,2],[3,4]]
        if expression.startswith("[[") and expression.endswith("]]"):
            matrix = sp.Matrix(eval(expression))
            return str(matrix)

        # Replace common math names
        expr = expression.replace("^", "**")

        # Map of allowed symbols
        allowed = {
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "asin": sp.asin,
            "acos": sp.acos,
            "atan": sp.atan,
            "log": sp.log,
            "ln": sp.ln,
            "exp": sp.exp,
            "sqrt": sp.sqrt,
            "pi": sp.pi,
            "e": sp.E,
        }

        # Evaluate safely using sympy
        result = sp.sympify(expr, locals=allowed)
        simplified = sp.N(result)
        return str(simplified)
    except Exception as e:
        return f"Error: {e}"

@app.route("/calculator", methods=["GET", "POST"])
@login_required
def calculator():
    result = ""
    if request.method == "POST":
        expression = request.form["expression"]
        result = safe_evaluate(expression)
    return render_template("calculator.html", result=result, username=current_user.username)

# -------------------------------------------------------------------
# Run App
# -------------------------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ✅ fixed: runs inside context

    use_ssl = os.getenv("USE_SSL", "false").lower() == "true"
    if use_ssl:
        app.run(
            ssl_context=(os.getenv("SSL_CERT_PATH"), os.getenv("SSL_KEY_PATH")),
            debug=True
        )
    else:
        app.run(debug=True)
