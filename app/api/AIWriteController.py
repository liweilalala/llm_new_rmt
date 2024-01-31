from flask import request
import datetime
from . import api
from app.api.AllTypes import Conference, LeaderSpeech, StrategicSigning, Exhibition
import json
from flask_jwt_extended import jwt_required, get_jwt
from ..utils import log


@api.route('/api/generate', methods=['POST'])
@jwt_required()
def ai_write():
    data_raw = request.get_data()
    timestamp_now = datetime.datetime.timestamp(datetime.datetime.now().replace(microsecond=0))
    expired_timestamp = get_jwt().get("expired_timestamp")
    log.info(type(expired_timestamp))
    log.info(expired_timestamp)
    remain_seconds = expired_timestamp-timestamp_now
    try:
        data = json.loads(data_raw)
    except json.decoder.JSONDecodeError as e:
        return json.dumps({"code": 403, "data": None, "msg": "格式错误"}, ensure_ascii=False), 403
    type_list = [None, Conference, LeaderSpeech, StrategicSigning, Exhibition]
    try:
        data_type = type_list[int(data["type"])]()
        result = data_type.generate(user_input=data["input"])
    except Exception as e:
        log.error(f"生成失败，原因：{e}")
        return json.dumps({"code": 405, "msg": f"生成失败，原因：{e}"}, ensure_ascii=False), 405
    result_dict = {"code": 200, "data": {"output": result}, "token_remain_seconds": remain_seconds, "msg": "生成成功"}
    return json.dumps(result_dict, ensure_ascii=False), 200
