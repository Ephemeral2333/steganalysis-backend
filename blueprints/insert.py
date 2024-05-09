import os
import random
import shlex
import time

import pandas as pd
from flask import Blueprint, jsonify
from flask import request
import subprocess

bp = Blueprint('insert', __name__, url_prefix='/steganography')


@bp.route('/insertInfo', methods=['POST'])
def insertInfo():
    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({
            'code': 400,
            'message': '未上传图片'
        })
    file = request.files['file']
    radio = request.form.get('radio')
    alpha = request.form.get('alpha')

    # 实现图片隐写
    save_file_path = 'steganography/image/cover/' + file.filename
    cover_file_path = '"' + 'steganography/image/cover' + '"'
    stego_file_path = '"' + 'steganography/image/stego' + '"'
    file.save(save_file_path)
    method = ''

    if radio == '1':
        method = 'HUGO_like'
    elif radio == '2':
        method = 'WOW'
    elif radio == '3':
        method = 'S-UNIWARD'

    cmd = './steganography/%s.exe -v -I "%s" -O "%s" -a %s' % (method, cover_file_path, stego_file_path, alpha)
    args = shlex.split(cmd)
    subprocess.run(args, shell=False, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 将隐写后的图片上传到七牛云
    from utils.QiniuTool import QiniuTool
    res = QiniuTool().upload(open('steganography/image/stego/' + file.filename, 'rb').read(),
                             'steganography/' + str(int(time.time())) + '_' + file.filename)

    # 删除本地文件
    os.remove('steganography/image/cover/' + file.filename)
    os.remove('steganography/image/stego/' + file.filename)

    return jsonify({
        'code': 200,
        'message': {
            'url': res
        }
    })

