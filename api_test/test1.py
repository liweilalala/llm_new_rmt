import requests
import json


base_url = "http://127.0.0.1:8002/"


def api_test(my_api: str, method: str, data: dict):
    url = base_url + my_api
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMDEyMjg1MiwianRpIjoiNDRiYWM3ZDgtMzA1OC00NDBlLWI1N2ItYTI2OTQ5ZmI4MjVlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QiLCJuYmYiOjE3MDAxMjI4NTIsImV4cCI6MTcwMDk4Njg1Mn0._JBcfzI2EW7ue_MehQ51nFvrSEG5HGVOlWsPxkOBxRU"
    }
    if method == "POST":
        result = requests.post(url, data=json.dumps(data), headers=headers, timeout=3000)

        try:
            result_data = json.loads(result.text)
        except:
            print("json解析失败")
            result_data = result.text
        print(result_data)
    else:
        return


if __name__ == "__main__":
    # data1 = {
    #     "user": "test",
    #     "passwd": "123456"
    # }
    data1 = {
        "title": "111",
        "type": 1,
        "input": "新华社旧金山11月15日电（记者倪四义　颜亮　吴晓凌）当地时间11月15日，国家主席习近平在美国旧金山斐洛里庄园同美国总统拜登举行中美元首会晤。两国元首就事关中美关系的战略性、全局性、方向性问题以及事关世界和平和发展的重大问题坦诚深入地交换了意见。"
    }
    api_test("api/generate", "POST", data1)

