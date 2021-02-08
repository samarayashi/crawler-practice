import requests

# 登入露天拍賣
session = requests.Session()

response = session.post(
    url='https://member.ruten.com.tw/user/login.php',
    headers={
        'Referer': 'https://member.ruten.com.tw/user/login.htm',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    },
    data={
        'userid': '<USERNAME>',
        'userpass': '<PASSWORD>'
    }
)
if response.status_code != 200:
    print(f'response status is not 200 ({response.status_code})')

with open('ruten.html', 'wb') as f:
    f.write(response.content)
