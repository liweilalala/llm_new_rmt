from flask import request, jsonify
from . import api
from app.api.AllTypes import Conference, LeaderSpeech, StrategicSigning, Exhibition
import json


@api.route('/api/generate', methods=['POST'])
def ai_write():
    data_raw = request.get_data()
    try:
        data = json.loads(data_raw)
    except json.decoder.JSONDecodeError as e:
        return jsonify({"code": 403, "data": None, "msg": "格式错误"}), 403
    type_list = [None, Conference, LeaderSpeech, StrategicSigning, Exhibition]
    try:
        data_type = type_list[int(data["type"])]()
        result = data_type.generate(user_input=data["input"])
    except Exception as e:
        print(f"生成失败，原因：{e}")
        return jsonify({"code": 405, "msg": f"生成失败，原因：{e}"}), 405
    return jsonify({"code": 200, "data": {"output": result}, "msg": "生成成功"})
