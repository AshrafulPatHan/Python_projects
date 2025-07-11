from flask import Blueprint,render_template

page_bp = Blueprint('page',__name__,url_prefix='/page')

# 📜 Login
@page_bp.route('/login')
def Login_page():
    return render_template("./page/login.html")

# 📜 register
@page_bp.route('/register')
def register_page():
    return render_template("./page/register.html")

# 📜 Book
@page_bp.route('/book')
def book_page():
    return render_template("./page/book.html")

# 📜 Admin
@page_bp.route('/admin')
def admin_page():
    return render_template("./page/admin.html")

