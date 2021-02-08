
import requests
import requests.utils
import loguru

# let session to manage cookie
# only need csrftoken and SPC_F
# ex: cookie = 'csrftoken=KQZxcU2TsIdFmkfUHt4uJeo5TYq5WUkl; SPC_F=hkBgxoMXveYbIXT13dTFw0u819bt5AdN;'

cookie = 'csrftoken=<CSRF-TOEKN>; SPC_F=<SPC_F>'
cookie = [
    item.strip()
    for item in cookie.split(';')
    if item.strip()
]
cookie = [
    item.split('=')
    for item in cookie
]
cookie = dict(cookie)
cookies = requests.utils.cookiejar_from_dict(cookie)

session = requests.Session()
session.cookies = cookies

# from login api
response = session.post(
    url='https://shopee.tw/api/v2/authentication/login',
    headers={
        'referer': 'https://shopee.tw/buyer/login',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'x-csrftoken': '<x-csrftoken>'
        # 'x-csrftoken': 'KQZxcU2TsIdFmkfUHt4uJeo5TYq5WUkl'
    },
    # put the content of Request Payload here
    json={"username": "<usernanme>",
          "password": "<hash_password>",
          "support_whats_app": True,
          "support_ivs": True}
)

# write buyer-response into shopee.buyer.login.json
if response.status_code != 200:
    loguru.logger.warning(
        f' buyer-api response status is not 200 ({response.status_code})')
else:
    loguru.logger.success('get buyer-api respose')

with open('shopee.buyer.login.json', 'wb') as f:
    f.write(response.content)

# keep login statement, requst seller-api
response = session.get('https://seller.shopee.tw/api/v2/login/')
if response.status_code != 200:
    loguru.logger.warning(
        f' seller-api response status is not 200 ({response.status_code})')
else:
    loguru.logger.success('get seller-api respose')

with open('shopee.seller.login.json', 'wb') as f:
    f.write(response.content)

#  grab the home-page, after login successfully
response = requests.get('https://shopee.tw/')
if response.status_code != 200:
    loguru.logger.warning(
        f' home-page response status is not 200 ({response.status_code})')
else:
    loguru.logger.success('get home-page respose')

with open('shopee.login.homepage.html', 'wb') as f:
    f.write(response.content)
