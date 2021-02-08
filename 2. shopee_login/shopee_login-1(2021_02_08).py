
import requests
import requests.utils
import json

response = requests.post(
    url='https://shopee.tw/api/v2/authentication/login',
    headers={
        'cookie': 'csrftoken=KQZxcU2TsIdFmkfUHt4uJeo5TYq5WUkl; SPC_F=hkBgxoMXveYbIXT13dTFw0u819bt5AdN;',
        'referer': 'https://shopee.tw/buyer/login',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'x-csrftoken': 'KQZxcU2TsIdFmkfUHt4uJeo5TYq5WUkl'
    },
    json={"username": "andychen208", "password": "21c03f30d2dbfd3d6da274dbc436a81e1c0dbffcb70734d92d4f7675aee0d566",
          "support_whats_app": True, "support_ivs": True}
    # data=json.dumps({"username": "andychen208",
    #                  "password": "21c03f30d2dbfd3d6da274dbc436a81e1c0dbffcb70734d92d4f7675aee0d566",
    #                  "support_whats_app": True, "support_ivs": True})

)
if response.status_code != 200:
    print(f'response status is not 200 ({response.status_code})')

# 輸出login後的response內容
with open('shopee.buyer.login.json', 'wb') as f:
    f.write(response.content)

#  登入成功後，再去一次首頁把內容拉下來
response = requests.get('https://shopee.tw/')
if response.status_code != 200:
    print(f'response status is not 200 ({response.status_code})')

with open('shopee.seller.login.html', 'wb') as f:
    f.write(response.content)
