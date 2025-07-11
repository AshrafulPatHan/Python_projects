from flask import Blueprint

public_bp = Blueprint('public',__name__,url_prefix='/')

@public_bp.route('/start')
def start():
    return "the server is start on update:1.2"

