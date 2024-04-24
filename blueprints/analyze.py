import io
from exts import mail
from utils import captcha, predict_image
from flask import Blueprint, jsonify
from flask import request
from PIL import Image
from flask_mail import Message

from utils.QiniuTool import QiniuTool

bp = Blueprint('analyze', __name__, url_prefix='/analyze')


@bp.route('/result', methods=['POST'])
def result():
    if 'file' not in request.files:
        return jsonify({
            'code': 400,
            'message': 'No file part'
        })
    file = request.files['file']

    # 判断隐写图像
    image_bytes = file.read()

    # 图片上传到七牛云
    res = QiniuTool().upload(image_bytes, file.filename)
    print(res)

    image = Image.open(io.BytesIO(image_bytes))
    result = predict_image.predict(image)

    if result == 0:
        return jsonify({
            'code': 200,
            'message': '非隐写图片'
        })
    else:
        return jsonify({
            'code': 200,
            'message': '隐写图片'
        })
