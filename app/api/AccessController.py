from flask import request, jsonify
from . import api
import json
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required, get_jwt
from constants import user, passwd


@api.route('/api/getToken', methods=['POST'])
def login():
    data_raw = request.get_data()
    try:
        data = json.loads(data_raw)
    except json.decoder.JSONDecodeError as e:
        return jsonify({"code": 403, "data": None, "msg": "格式错误"}), 403
    if data['user'] == user and data['passwd'] == passwd:
        access_token = create_access_token(identity=data["user"])
        return jsonify({"code": 200, "data": {"token": access_token}, "msg": "请求成功"})
    else:
        print("用户名或密码错误")
        return jsonify({"code": 406, "msg": "用户名或密码错误"}), 406



