# python3 app.py

from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
from dotenv import load_dotenv
from routes.auth.routes import auth_bp
from routes.admin.routes import admin_bp
from routes.public.routes import public_bp
from routes.page.routes import page_bp
import os
from DB import mysql, init_app


# Load env variables
load_dotenv()

app = Flask(__name__)
CORS(app)
init_app(app)

app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))

Owner = """
 █████╗ ███████╗██╗  ██╗██████╗  █████╗ ███████╗██╗   ██╗██╗     
██╔══██╗██╔════╝██║  ██║██╔══██╗██╔══██╗██╔════╝██║   ██║██║     
███████║███████╗███████║██████╔╝███████║█████╗  ██║   ██║██║     
██╔══██║╚════██║██╔══██║██╔══██╗██╔══██║██╔══╝  ██║   ██║██║     
██║  ██║███████║██║  ██║██║  ██║██║  ██║██║     ╚██████╔╝███████╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝

"""
print(Owner)

# 🖥️ start the server
@app.route('/', methods=['GET'])
def Start_server():
    result = "server is running"
    return jsonify(result)

# 📄 html website
@app.route('/site')
def HTML_SERVER():
    return render_template("index.html")

# 🧭 routes
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(public_bp)
app.register_blueprint(page_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5000)