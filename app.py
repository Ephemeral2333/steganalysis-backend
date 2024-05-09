from flask import Flask, jsonify
import config
from exts import db, mail
from blueprints.analyze import bp as analyze_bp
from blueprints.login import bp as login_bp
from blueprints.insert import bp as insert_bp
from blueprints.history import bp as history_bp
from blueprints.test import bp as test_bp
from blueprints.data import bp as data_bp
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
app.register_blueprint(analyze_bp)
app.register_blueprint(login_bp)
app.register_blueprint(insert_bp)
app.register_blueprint(history_bp)
app.register_blueprint(test_bp)
app.register_blueprint(data_bp)


# 在每个请求之后添加 CORS 头
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With, Authorization, Email'
    return response


# 如果作为主程序运行，启动应用
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003, debug=True)
