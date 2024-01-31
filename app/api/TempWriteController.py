from flask import request
from . import api
from app.api.AllTypes import Conference, LeaderSpeech, StrategicSigning, Exhibition
from app.utils.LLM import create_task_loop, use_llm
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
    remain_seconds = expired_timestamp - timestamp_now
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
    return json.dumps({"code": 200, "data": {"output": result}, "token_remain_seconds": remain_seconds, "msg": "生成成功"},
                      ensure_ascii=False), 200


@api.route('/api/template2/generate', methods=['POST'])
@jwt_required()
def temp_write2():
    data_raw = request.get_data()
    timestamp_now = datetime.datetime.timestamp(datetime.datetime.now().replace(microsecond=0))
    expired_timestamp = get_jwt().get("expired_timestamp")
    remain_seconds = expired_timestamp - timestamp_now
    try:
        data = json.loads(data_raw)
    except json.decoder.JSONDecodeError as e:
        return json.dumps({"code": 403, "data": None, "msg": f"格式错误，{e}"}, ensure_ascii=False), 403
    temp_doc_generators = {"1": frame_copywrite, "2": style_copywrite}
    this_generate = temp_doc_generators[str(data["method"])]
    try:
        best_result: dict = this_generate(temp_content=data['temp_content'],
                                          user_input=data["user_input"])
    except Exception:
        return json.dumps({"code": 405, "data": None, "msg": "模板生成结果失败"}, ensure_ascii=False), 405
    if len(best_result['answer']) < 10:
        return json.dumps({"code": 405, "data": None, "msg": "模板生成结果失败"}, ensure_ascii=False), 405
    return json.dumps({"code": 200, "data": {"output": best_result['answer']},
                       "token_remain_seconds": remain_seconds,
                       "msg": "生成成功"}, ensure_ascii=False), 200


def frame_copywrite(temp_content: str, user_input: str):
    prompt2 = '请以下面文章为样例，总结此种类型文章的框架结构，禁止出现文章具体内容，不要举例：\n'
    kuangjia = use_llm(
        my_text=prompt2 + temp_content,
        url="http://10.10.1.101:14240/continue_write")  # 总结框架
    log.info('框架如下\n' + kuangjia['answer'])
    kuangjiagaixiehou = use_llm(
        my_text='请使用以下框架对素材进行改写，生成一篇正式的文章。框架：｛{}｝。素材：｛{}｝。'.format(kuangjia['answer'], user_input),
        url="http://10.10.1.102:14247/continue_write")
    log.info('框架仿写后文章如下\n' + kuangjiagaixiehou['answer'])
    return kuangjiagaixiehou


def style_copywrite(temp_content: str, user_input: str):
    prompt2 = '请以下面文章为样例，总结此种类型文章的语言风格、情感色彩、叙述方式、文风特点、表达方式、文章写作风格。禁止出现文章具体内容，不要举例：\n'
    wenfeng = use_llm(
        my_text=prompt2 + temp_content,
        url="http://10.10.1.101:14240/continue_write")  # 总结框架
    log.info('文风如下\n' + wenfeng['answer'])
    wenfenggaixiehou = use_llm(
        my_text='请按照要求改写以下文章的文风，保留文章的内容。\n文章：｛{}｝。\n文风要求：｛{}｝。'.format(user_input, wenfeng['answer']),
        url="http://10.10.1.101:14240/continue_write")
    log.info('文风仿写后文章如下\n' + wenfenggaixiehou['answer'])
    return wenfenggaixiehou
