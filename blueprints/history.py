import io
import time
from flask import Blueprint, jsonify, session, make_response
from flask import request
from PIL import Image
from exts import db
from models.History import History
from utils.QiniuTool import QiniuTool

bp = Blueprint('history', __name__, url_prefix='/history')


@bp.before_request
def before_request():
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
    query = request.args.get('query')
    pagenum = request.args.get('pagenum')
    pagesize = request.args.get('pagesize')
    result = []
    page_total = None
    from models.User import User
    email = request.headers.get('Email')

    if query:
        # 查找到所有result或u_result为query的记录
        user = User.query.filter(User.email == email).first()
        query_result = History.query.filter(History.user_id == user.id).filter(
            (History.result == query) | (History.u_result == query)).order_by(History.created_time.desc()).paginate(
            page=int(pagenum), per_page=int(pagesize), error_out=False)
    else:
        user = User.query.filter(User.email == email).first()
        query_result = History.query.filter(History.user_id == user.id).order_by(History.created_time.desc()).paginate(
            page=int(pagenum), per_page=int(pagesize), error_out=False)
    page_total = query_result.pages
    history = query_result.items
    for h in history:
        result.append({
            'id': h.id,
            'image': h.image,
            'image_show': h.image_show,
            'result': h.result,
            'u_result': True if h.u_result == 1 else False,
            'created_time': h.created_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({
        'code': 200,
        'data': {
            'total': page_total,
            'items': result
        }
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


@bp.route('/change', methods=['PUT'])
def history_change():
    from models.History import History

    history_id = request.get_json().get('id')
    history = History.query.filter(History.id == history_id).first()
    if history.u_result == 1:
        history.u_result = 0
    else:
        history.u_result = 1

    db.session.commit()
    return jsonify({
        'code': 200,
        'message': history.u_result
    })


@bp.route('/compare', methods=['GET'])
def history_compare():
    from models.History import History
    email = request.headers.get('Email')
    from models.User import User
    user = User.query.filter(User.email == email).first()

    history = History.query.filter(History.user_id == user.id).all()
    same, diff = 0, 0
    cover, stego = 0, 0

    for h in history:
        if h.u_result != h.result:
            diff += 1
        else:
            same += 1
        if h.result:
            stego += 1
        else:
            cover += 1

    return jsonify({
        'code': 200,
        'data': {
            'same': same,
            'diff': diff,
            'result': [cover, stego]
        }
    })


# 导出excel
@bp.route('/export', methods=['GET'])
def history_export():
    from models.History import History
    email = request.headers.get('Email')
    from models.User import User
    user = User.query.filter(User.email == email).first()

    history = History.query.filter(History.user_id == user.id).all()
    import xlwt
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Sheet1')

    worksheet.write(0, 0, 'ID')
    worksheet.write(0, 1, '是否隐写')
    worksheet.write(0, 2, '用户判断')
    worksheet.write(0, 3, '分析时间')
    worksheet.write(0, 4, '图片URL')

    for index, h in enumerate(history):
        worksheet.write(index + 1, 0, h.id)
        worksheet.write(index + 1, 1, '是' if h.result else '否')
        worksheet.write(index + 1, 2, '是' if h.u_result else '否')
        worksheet.write(index + 1, 3, h.created_time.strftime('%Y-%m-%d %H:%M:%S'))
        worksheet.write(index + 1, 4, h.image)

    # 返回二进制流
    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    # 创建响应对象
    response = make_response(output.getvalue())

    # 设置Content-Type和Content-Disposition头信息
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'attachment; filename="repair.xls"'

    return response
