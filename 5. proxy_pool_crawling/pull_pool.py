import requests
import csv

import pyquery
import munch

response = requests.get(
    url='https://free-proxy-list.net/'
)


if response.status_code != 200:
    print(f'response status is not 200 ({response.status_code})')

with open('free-proxy.html', 'wb') as f:
    f.write(response.content)

proxies = []
dom = pyquery.PyQuery(response.text)
table_list = dom('table#proxylisttable')
trs = table_list('tbody > tr').items()
for tr in trs:
    tds = list(tr('td').items())
    ip = tds[0].text()
    port = tds[1].text()
    print(f'{ip}\t{port}')
    proxies.append(munch.munchify({
        'ip': ip,
        'port': port
    }))

with open('proxies.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'IP',
        'PORT'
    ])
    for proxy in proxies:
        writer.writerow([
            proxy.ip,
            proxy.port
        ])
