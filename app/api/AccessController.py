from flask import request, jsonify
import datetime
from . import api
import json
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required, get_jwt
from .constants import user, passwd
from ..utils import log


@api.route('/api/getToken', methods=['POST'])
def login():
    log.info("接收到请求")
    data_raw = request.get_data()
    log.info(data_raw)
    try:
        data = json.loads(data_raw)
    except json.decoder.JSONDecodeError as e:
        log.error(f"格式错误：{e}")
        return json.dumps({"code": 403, "data": None, "msg": "格式错误"}, ensure_ascii=False), 403
    if data['user'] == user and data['passwd'] == passwd:
        create_time = datetime.datetime.now().replace(microsecond=0) 
        expired_timestamp = datetime.datetime.timestamp(create_time + datetime.timedelta(days=10))
        access_token = create_access_token(identity=data["user"], 
                                           additional_claims={'expired_timestamp': expired_timestamp})
        return json.dumps({"code": 200, 
                           "data": {"token": access_token},
                           "token_remain_seconds": datetime.timedelta(days=10).total_seconds(),
                           "msg": "请求成功"}, ensure_ascii=False)
    else:
        log.error("用户名或密码错误")
        return json.dumps({"code": 406, "msg": "用户名或密码错误"}, ensure_ascii=False), 406


@api.route('/api/test', methods=['POST'])
@jwt_required()
def test():
    return jsonify({})


