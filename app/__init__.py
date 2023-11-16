from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
import datetime


def create_app():
    app = Flask(__name__)
    # 设置好jwt加密用的key
    app.config["JWT_SECRET_KEY"] = "khMm2pEemLaF7pRw"
    app.config['SECRET_KEY'] = "HRuUpy4tOQSMBFWw"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=10)
    register_blueprint(app)
    jwt = JWTManager()

    @jwt.expired_token_loader
    def my_expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"code": 401, "msg": "token已过期，请重新获取。"}), 401

    jwt.init_app(app)
    return app


def register_blueprint(app):
    from .api import api
    app.register_blueprint(api)
