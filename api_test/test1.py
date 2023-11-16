import requests
import json


base_url = "http://127.0.0.1:8002/"


def api_test(my_api: str, method: str, data: dict):
    url = base_url + my_api
    headers = {
        "Content-Type": "application/json; charset=UTF-8"
    }
    if method == "POST":
        result = requests.post(url, data=json.dumps(data), headers=headers, timeout=3000)
        print(result.text)
        print(result.content)
    else:
        return


if __name__ == "__main__":
    data1 = {
        "user": "test",
        "passwd": "123456"
    }
    api_test("api/getToken", "POST", data1)

