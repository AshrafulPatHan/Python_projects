from flask import request,Blueprint,jsonify
from DB import mysql, init_app
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
    result = cursor.fetchone()

    # data is coming for database:
    user = {
        "id": result[0],
        "username": result[1],
        "email": result[2],
        "password": result[3],
        "role": result[4]
    }
    cursor.close()

    if user and check_password_hash(user['password'], password):
        # You can generate a session or JWT token here if needed
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user['id'],
                "username": user['username'],
                "email": user['email'],
                "role": user['role']
            }
        }), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401


@auth_bp.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    name = data['username']
    email = data['email']
    # password = data['password']
    # hashed password registration
    password = generate_password_hash(data['password'])
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
