from flask import request,Blueprint,jsonify
from DB import mysql, init_app

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    return "Login Page"

@auth_bp.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    name = data['username']
    email = data['email']
    password = data['password']
    role = 'user'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO Users (username, email, password, role) VALUES (%s, %s, %s, %s)",
        (name, email, password, role)
    )
    mysql.connection.commit()
    cursor.close()
    result= jsonify({"message":"User is add successfully"}), 201
    return result
