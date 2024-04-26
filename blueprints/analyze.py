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

    image_show_url = ''

    # 判断隐写图像
    image_bytes = file.read()

    # 图片上传到七牛云
    res = QiniuTool().upload(image_bytes, 'steganalysis/' + str(int(time.time())) + '_' + file.filename)
    image = Image.open(io.BytesIO(image_bytes))
    result = predict_image.predict(image)

    # 若图片为.pgm格式，则将文件重命名为.png格式
    if file.filename.endswith('.pgm'):
        file.filename = file.filename.replace('.pgm', '.png')
        image.save(file.filename)
        image_show_url = QiniuTool().upload(open(file.filename, 'rb').read(), 'steganalysis/' + str(int(time.time())) + '_' + file.filename)
    else:
        image_show_url = res

    print('image_show_url:', image_show_url)

    if result == 0:
        return jsonify({
            'code': 200,
            'message': {
                'result': '正常图片',
                'url': res,
                'jpeg_url': image_show_url
            }
        })
    else:
        return jsonify({
            'code': 200,
            'message': {
                'result': '隐写图片',
                'url': res,
                'jpeg_url': image_show_url
            }
        })
