from flask import request, jsonify
from . import api
from app.api.AllTypes import Conference, LeaderSpeech, StrategicSigning, Exhibition
from app.utils.LLM import create_task_loop
from .AllTypes.new_prompt import generate_prompt
import json


@api.route('/api/template/generate', methods=['POST'])
def temp_write():
    data_raw = request.get_data()
    try:
        data = json.loads(data_raw)
    except json.decoder.JSONDecodeError as e:
        return jsonify({"code": 403, "data": None, "msg": f"格式错误，{e}"}), 403
    try:
        temp_prompts = generate_prompt(temp_text=data['temp_content'])
        query_list = []
        error_prompt_count = 0
        for prompt in temp_prompts:
            if prompt.instruction.startswith("<!doctype html>"):
                error_prompt_count += 1
                pass
            one_query = prompt.instruction + "请根据以上文本风格和特征，改写下面这篇文章，使其符合相似的风格。" + data[
                "user_input"]
            query_list.append(one_query)
        result = create_task_loop(query_list)
    except Exception as e:
        print(f"模板生成失败，原因：{e}")
        try:
            type_list = [None, Conference, LeaderSpeech, StrategicSigning, Exhibition]
            data_type = type_list[int(data["temp_type"])]()
            result = data_type.generate(user_input=data["user_input"])
        except Exception as e1:
            print(f"生成失败，原因：{e1}")
            return jsonify({"code": 405, "msg": f"生成失败，原因：{e1}"}), 405

    return jsonify({"code": 200, "data": {"output": result}, "msg": "生成成功"})
