import requests
import json


base_url = "http://127.0.0.1:8002/"


def api_test(my_api: str, method: str, data: dict):
    url = base_url + my_api
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        # "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMDEyMDg1NywianRpIjoiZWVkNTRmYjgtODdkYi00NmEzLTlkY2EtMmVmZmJhNGQ3OWRiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QiLCJuYmYiOjE3MDAxMjA4NTcsImV4cCI6MTcwMDEyMDkxN30.hgSQBNTa-9i0X5vYudRNXs13G5gMxXqIzmoexE5U58Y"
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
    data1 = {
        "user": "test",
        "passwd": "123456"
    }
    # data1 = {}
    api_test("api/test", "POST", data1)

