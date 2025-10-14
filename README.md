🧮 SmartCalc — Flask-based Secure Web Calculator

SmartCalc is a **Flask web application** that combines secure user authentication and advanced mathematical computation using **Sympy** and **NumPy**.  
It supports standard, trigonometric, inverse, logarithmic, exponential, and matrix calculations — all in a modern web interface.



🚀 Features

✅ User Registration & Login (with hashed passwords)  
✅ SQLite database with SQLAlchemy ORM  
✅ Trigonometric and inverse trig functions (`sin`, `asin`, etc.)  
✅ Logarithmic, exponential, and square root operations  
✅ Matrix operations (`[[1,2],[3,4]]`)  
✅ Safe Sympy-based expression evaluator  
✅ Flask + Flask-Login + Flask-SQLAlchemy  
✅ Simple, modern, responsive UI  
✅ SSL-ready configuration via `.env`



🏗️ Project Structure

Calculator/
├── app1.py
├── requirements.txt
├── .env.example
├── templates/
│ ├── login.html
│ ├── register.html
│ ├── calculator.html
└── static/
└── style.css
└── calculator.js
