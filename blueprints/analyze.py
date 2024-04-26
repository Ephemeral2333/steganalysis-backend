import io
import time
from utils import predict_image
from flask import Blueprint, jsonify, session
from flask import request
from PIL import Image

from utils.QiniuTool import QiniuTool

bp = Blueprint('analyze', __name__, url_prefix='/analyze')

@bp.before_request
def before_request():
    token = request.headers.get('Authorization')

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
    res = QiniuTool().upload(image_bytes, 'steganalysis/' + str(int(time.time())) + '_' + file.filename)

    image = Image.open(io.BytesIO(image_bytes))
    result = predict_image.predict(image)

    if result == 0:
        return jsonify({
            'code': 200,
            'message': {
                'result': '正常图片',
                'url': res
            }
        })
    else:
        return jsonify({
            'code': 200,
            'message': {
                'result': '隐写图片',
                'url': res
            }
        })
