from flask import request
from . import api
from app.api.AllTypes import Conference, LeaderSpeech, StrategicSigning, Exhibition
from app.utils.LLM import create_task_loop
from .AllTypes.new_prompt import generate_prompt
import json
from flask_jwt_extended import jwt_required, get_jwt
import datetime
from ..utils import log


@api.route('/api/template/generate', methods=['POST'])
@jwt_required()
def temp_write():
    data_raw = request.get_data()
    timestamp_now = datetime.datetime.timestamp(datetime.datetime.now().replace(microsecond=0))
    expired_timestamp = get_jwt().get("expired_timestamp")
    log.info(type(expired_timestamp))
    log.info(expired_timestamp)
    remain_seconds = expired_timestamp-timestamp_now
    try:
        data = json.loads(data_raw)
    except json.decoder.JSONDecodeError as e:
        return json.dumps({"code": 403, "data": None, "msg": f"格式错误，{e}"}, ensure_ascii=False), 403
    try:
        temp_prompts = generate_prompt(temp_text=data['temp_content'])
        log.info(f"prompts生成结果：{temp_prompts}")
        query_list = []
        error_prompt_count = 0
        for prompt in temp_prompts:
            if prompt['instruction'].startswith("<!doctype html>"):
                error_prompt_count += 1
                pass
            one_query = prompt['instruction'] + "请根据以上文本风格和特征，改写下面这篇文章，使其符合相似的风格。" + data["user_input"]
            query_list.append(one_query)
        result = create_task_loop(query_list)['answer']
    except Exception as e:
        log.info(f"模板生成失败，原因：{e}")
        try:
            type_list = [None, Conference, LeaderSpeech, StrategicSigning, Exhibition]
            data_type = type_list[int(data["temp_type"])]()
            result = data_type.generate(user_input=data["user_input"])
        except Exception as e1:
            log.info(f"生成失败，原因：{e1}")
            return json.dumps({"code": 405, "msg": f"生成失败，原因：{e1}"}, ensure_ascii=False), 405
    return json.dumps({"code": 200, "data": {"output": result}, "token_remain_seconds": remain_seconds, "msg": "生成成功"}, ensure_ascii=False)
