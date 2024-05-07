import io
import time
from flask import Blueprint, jsonify, session
from flask import request
from PIL import Image
from exts import db
from utils.QiniuTool import QiniuTool

bp = Blueprint('history', __name__, url_prefix='/history')


@bp.before_request
def before_request():
    print(request.headers)
    token = request.headers.get('Authorization')
    email = request.headers.get('Email')

    import hashlib
    from flask import current_app
    if not token or not email or token != hashlib.md5(
            (email + current_app.config.get("SECRET_KEY")).encode()).hexdigest():
        return jsonify({
            'code': 400,
            'message': '登录信息已过期，请重新登录'
        })


@bp.route('/list', methods=['GET'])
def history_list():
    from models.History import History
    email = request.headers.get('Email')
    from models.User import User
    user = User.query.filter(User.email == email).first()
    if not user:
        return jsonify({
            'code': 400,
            'message': '用户不存在'
        })

    history = History.query.filter(History.user_id == user.id).all()
    history_list = []
    for h in history:
        history_list.append({
            'id': h.id,
            'result': h.result,
            'image': h.image,
            'image_show': h.image_show,
            'created_time': h.created_time.strftime('%Y-%m-%d %H:%M:%S'),
        })
    return jsonify({
        'code': 200,
        'data': history_list
    })


@bp.route('/delete', methods=['DELETE'])
def history_delete():
    from models.History import History
    email = request.headers.get('Email')
    from models.User import User
    user = User.query.filter(User.email == email).first()
    if not user:
        return jsonify({
            'code': 400,
            'message': '用户账号异常'
        })

    history_id = request.get_json().get('id')
    history = History.query.filter(History.id == history_id).first()
    if not history:
        return jsonify({
            'code': 400,
            'message': '历史记录不存在'
        })

    db.session.delete(history)
    db.session.commit()
    return jsonify({
        'code': 200,
        'message': '删除成功'
    })
