# python3 app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from DB import mysql, init_app


# Load env variables
load_dotenv()

app = Flask(__name__)
CORS(app)
init_app(app)

app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))

# 🖥️ start the server
@app.route('/', methods=['GET'])
def Start_server():
    result = "server is running"
    return jsonify(result)

# ✅ Create Todo
@app.route('/todo', methods=['POST'])
def add_todo():
    data = request.get_json()
    title = data['title']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO TodoData (title) VALUES (%s)", (title,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Todo Added Successfully'}), 201

# 📖 Read All Todos
@app.route('/todo', methods=['GET'])
def get_todos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM TodoData")
    todos = cursor.fetchall()
    cursor.close()
    result = [{'id': row[0], 'title': row[1]} for row in todos]
    return jsonify(result)

# ✏️ Update Todo
@app.route('/todo/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    new_title = data['title']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE TodoData SET title=%s WHERE id=%s", (new_title, id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Todo Updated Successfully'})

# ❌ Delete Todo
@app.route('/todo/<int:id>', methods=['DELETE'])
def delete_todo(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM TodoData WHERE id=%s", (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Todo Deleted Successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
