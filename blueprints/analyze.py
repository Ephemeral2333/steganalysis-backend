from exts import mail
from utils import captcha
from flask import Blueprint
from flask import request
from flask_mail import Message

bp = Blueprint('analyze', __name__, url_prefix='/analyze')


@bp.route('/result', methods=['POST'])
def result():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    print(file.filename)
    return file.filename
