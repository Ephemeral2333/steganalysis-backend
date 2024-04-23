from flask import Flask, jsonify
import config
from exts import db, mail
from blueprints.analyze import bp as analyze_bp

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
app.register_blueprint(analyze_bp)

# 在每个请求之后添加 CORS 头
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


# 定义一个简单的路由
@app.route('/api/data', methods=['GET'])
def get_data():
    # 创建一个字典作为模拟数据
    data = {
        "message": "Hello from Flask!",
        "items": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"}
        ]
    }
    # 将字典转为 JSON 并返回
    return jsonify(data)


# 如果作为主程序运行，启动应用
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003, debug=True)
