from flask_mail import Message, current_app
from exts import db, mail
from utils.captcha import getCaptcha

from flask import Blueprint, request, jsonify, session

bp = Blueprint('login', __name__, url_prefix='/login')


@bp.route('/getcap', methods=['POST'])
def getcap():
    email = request.get_json().get('email')
    captcha = getCaptcha()

    subject = 'Steganalysis | 隐写分析系统验证码'
    body = f"您好！欢迎使用隐写分析系统，您的验证码为：{captcha}，请注意：验证码为唯一登录凭证，请勿泄露给他人。"
    message = Message(subject=subject, recipients=[email], body=body)
    mail.send(message)

    # 插入到captcha表中
    from models.Captcha import Captcha
    from datetime import datetime
    captcha = Captcha(email=email, captcha=captcha, captcha_time=datetime.now())
    db.session.add(captcha)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': 'success'
    })


@bp.route('/valid', methods=['POST'])
def login():
    email = request.get_json().get('email')
    captcha = request.get_json().get('captcha')

    from models.Captcha import Captcha
    from datetime import datetime, timedelta
    res = Captcha.query.filter(Captcha.email == email, Captcha.captcha == captcha).first()
    if res and res.captcha_time + timedelta(minutes=5) > datetime.now():
        # 删除该邮箱下的所有验证码
        Captcha.query.filter(Captcha.email == email).delete()

        # 如果user表中没有该邮箱，则插入
        from models.User import User
        user = User.query.filter(User.email == email).first()
        if not user:
            user = User(email=email, join_date=datetime.now())
            db.session.add(user)

        import hashlib
        token = hashlib.md5((email + current_app.config.get("SECRET_KEY")).encode()).hexdigest()
        session['email'] = token

        db.session.commit()
        return jsonify({
            'code': 200,
            'message': {
                'email': email,
                'token': token
            }
        })
    else:
        return jsonify({
            'code': 400,
            'message': '验证码错误或已过期'
        })
