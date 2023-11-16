import requests
import json


base_url = "http://127.0.0.1:8002/"


def api_test(my_api: str, method: str, data: dict):
    url = base_url + my_api
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMDEyMDMzMywianRpIjoiMjk5Y2Y5NTgtYzM1Ni00YzI5LTg1NzAtNTA5OTYzNWI2ZjBlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QiLCJuYmYiOjE3MDAxMjAzMzMsImV4cCI6MTcwMDk4NDMzM30.fh3NcHlQqgTZfTghVaw_ByGC22Ia-al1WNyQpvzAG3A"
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
    data1 = {}
    api_test("api/test", "POST", data1)

