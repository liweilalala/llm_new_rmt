import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
import sys
import os


def use_llm(my_text: str, system_message: str = "") -> dict:

    url = "http://127.0.0.1:14240/continue_write"
    data = {
        "sents": my_text,
        "system": system_message,
        "usr": "rongmeiti",
        "region": "0"
    }
    headers = {
        "Content-Type": "application/json; charset=UTF-8"
    }
    new_message = {}
    try:
        result = requests.post(url, data=json.dumps(data), headers=headers, timeout=3000)
        if result.status_code in [500, 502]:
            print("LLM请求失败")
            new_message['answer'] = ""
            new_message['score'] = None
    except requests.exceptions.ConnectionError:
        print("LLM请求失败")
        new_message['answer'] = ""
        new_message['score'] = None
    except requests.exceptions.ReadTimeout:
        print("LLM请求失败")
        new_message['answer'] = ""
        new_message['score'] = None
    else:
        new_message['answer'] = result.text
        new_message['score'] = get_score(result.text)
    return new_message


def get_score(candidate: str):
    url = "http://10.10.1.102:14244/reward"
    judge_instruction = '''请撰写一篇会议类新闻稿件'''
    headers = {
        "Content-Type": "application/json; charset=UTF-8"
    }
    data = {
        "query": judge_instruction,
        "response": candidate,
        "usr": "rongmeiti",
        "region": "0"
    }
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers, timeout=3000)
    except requests.exceptions.ConnectionError:
        print("评分接口无法连接")
        return None
    except requests.exceptions.ReadTimeout:
        print("评分接口连接超时")
        return None
    if response.status_code in [500, 502]:
        print("评分接口连接失败")
        return None
    score = float(response.text)
    return score


def create_task(input_list: list, system_message: str = "", 
                use_concurrent: bool = True):
    t1 = time.time()
    results = []
    if use_concurrent:
        executor_pool = ThreadPoolExecutor(max_workers=len(input_list))
        results = executor_pool.map(use_llm, input_list, repeat(system_message))
        executor_pool.shutdown(wait=True)
    else:
        for text in input_list:
            result = use_llm(text, system_message=system_message)
            results.append(result)
    useful_results = [result for result in results if result["score"] is not None]
    # best_result = list(sorted(useful_results, key=lambda item: item["score"], reverse=True))[0]

    t2 = time.time()
    print("任务耗时：%f" % (t2-t1))
    return useful_results


def create_task_loop(input_list: list, system_message: str = "",
                     use_concurrent: bool = True):
    err_count = 0
    while True:
        results = create_task(input_list, system_message, use_concurrent)
        if len(results) > 1:
            best_result = list(sorted(results, key=lambda item: item["score"], reverse=True))[0]
            return best_result
        elif len(results) == 1:
            return results[0]
        else:
            err_count += 1
        
        if err_count >= 3:
            break
    return None

