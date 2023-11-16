from flask import Flask


def create_app():
    app = Flask(__name__)
    register_blueprint(app)
    return app


def register_blueprint(app):
    from .api import api
    app.register_blueprint(api)
