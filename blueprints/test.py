import datetime
import io
import os
from flask_mail import Message, current_app
from exts import db, mail
from utils.captcha import getCaptcha
from flask import Blueprint, request, jsonify, session, make_response
from utils.save_zip import unzip_file
from utils.test_model import test_model
from utils.QiniuTool import QiniuTool
import shutil
from models.testmodel import TestModel

bp = Blueprint('test', __name__, url_prefix='/test')


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

@bp.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return jsonify({'code': 400, 'msg': 'No file part'})
    date_now = datetime.datetime.now()
    date_str = date_now.strftime('%Y%m%d%H%M%S')
    filepath = 'upload/' + date_str + file.filename

    email = request.headers.get('Email')
    from models.User import User
    user = User.query.filter(User.email == email).first()
    from models.testmodel import TestModel
    testModel = TestModel(u_id=user.id, name=file.filename,
                          precision=-1, recall=-1, f1=-1, accuracy=-1, created_time=date_now)
    db.session.add(testModel)
    db.session.commit()

    file.save(filepath)

    res = QiniuTool().upload_path(filepath, 'testmodel/' + date_str + file.filename)
    unzip_path = 'upload/unzip/' + file.filename.split('.')[0] + date_str
    unzip_file(filepath, unzip_path)

    # 测试模型
    try:
        precision, recall, f1_score, accuracy = test_model(unzip_path)
        testModel.assign(res, precision, recall, f1_score, accuracy)
    except Exception as e:
        testModel.state = -1
        testModel.url = res
        db.session.commit()

    # 删除临时文件
    os.remove(filepath)
    shutil.rmtree(unzip_path)

    return jsonify({'code': 200, 'msg': 'Upload success'})


@bp.route('/list', methods=['GET'])
def list():
    query = request.args.get('query')
    pagenum = request.args.get('pagenum')
    pagesize = request.args.get('pagesize')
    result = []
    page_total = None
    from models.User import User
    email = request.headers.get('Email')

    if query:
        user = User.query.filter(User.email == email).first()
        query_result = TestModel.query.filter(TestModel.u_id == user.id).filter(TestModel.name.like('%' + query + '%')).order_by(
            TestModel.created_time.desc()).paginate(
            page=int(pagenum), per_page=int(pagesize), error_out=False)
    else:
        user = User.query.filter(User.email == email).first()
        query_result = TestModel.query.filter(TestModel.u_id == user.id).order_by(TestModel.created_time.desc()).paginate(
            page=int(pagenum), per_page=int(pagesize), error_out=False)
    page_total = query_result.pages
    testmodel = query_result.items
    for t in testmodel:
        result.append({
            'id': t.id,
            'url': t.url,
            'name': t.name,
            'precision': t.precision,
            'recall': t.recall,
            'f1': t.f1,
            'accuracy': t.accuracy,
            'state': t.state,
            'created_time': t.created_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({
        'code': 200,
        'data': {
            'total': page_total,
            'items': result
        }
    })


# 导出excel
@bp.route('/export', methods=['GET'])
def export():
    import xlwt
    email = request.headers.get('Email')
    from models.User import User
    user = User.query.filter(User.email == email).first()

    from models.testmodel import TestModel
    testmodel = TestModel.query.filter(TestModel.u_id == user.id).all()

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('testmodel')

    worksheet.write(0, 0, 'id')
    worksheet.write(0, 1, 'url')
    worksheet.write(0, 2, 'name')
    worksheet.write(0, 3, 'precision')
    worksheet.write(0, 4, 'recall')
    worksheet.write(0, 5, 'f1')
    worksheet.write(0, 6, 'accuracy')
    worksheet.write(0, 7, 'created_time')

    for i, t in enumerate(testmodel):
        worksheet.write(i + 1, 0, t.id)
        worksheet.write(i + 1, 1, t.url)
        worksheet.write(i + 1, 2, t.name)
        worksheet.write(i + 1, 3, t.precision)
        worksheet.write(i + 1, 4, t.recall)
        worksheet.write(i + 1, 5, t.f1)
        worksheet.write(i + 1, 6, t.accuracy)
        worksheet.write(i + 1, 7, t.created_time.strftime('%Y-%m-%d %H:%M:%S'))

    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    # 创建响应对象
    response = make_response(output.getvalue())

    # 设置Content-Type和Content-Disposition头信息
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'attachment; filename="repair.xls"'

    return response
