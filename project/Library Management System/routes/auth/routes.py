from flask import request,Blueprint,jsonify,make_response
import jwt
import datetime
from DB import mysql, init_app
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os



load_dotenv()
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
SECRET_KEY = os.getenv('JWT_KEY')


# 📜 login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return jsonify({"message": "Invalid credentials"}), 401

    user = {
        "id": result[0],
        "username": result[1],
        "email": result[2],
        "password": result[3],
        "role": result[4]
    }

    if check_password_hash(user['password'], password):
        token_payload = {
            "user_id": user["id"],
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=365)
        }

        token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

        response = make_response(jsonify({"message": "Login successful"}), 200)
        response.set_cookie(
            "token",
            token,
            httponly=True,
            samesite='Lax',  #  'Strict'or 'None'
            max_age=60 * 60 * 24 * 365  # work for 1 year
        )

        return response
    else:
        return jsonify({"message": "Invalid email or password"}), 401

# 📜 register
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

# 📜 profile
@auth_bp.route('/profile', methods=['GET'])
def profile():
    token = request.cookies.get('token')

    if not token:
        return jsonify({"message": "Unauthorized"}), 401

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({
            "message": "User is logged in",
            "user": {
                "user_id": decoded['user_id'],
                "email": decoded['email']
            }
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

# 📜 logout
@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({"message": "Logged out"}), 200)
    response.set_cookie('token', '', expires=0)
    return response

