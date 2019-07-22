import requests
import json

url = "http://bigpara.hurriyet.com.tr/api/v1/hisse/list"

headers = {
    'cache-control': "no-cache",
    'postman-token': "fb97e4a7-abc8-7a00-a116-2ecc1ae88d07"
}

response = requests.request("GET", url, headers=headers)

j = json.loads(response.text)

print(response.text)