import requests
from bs4 import BeautifulSoup

import pandas as pd
url = 'https://finance.naver.com/'

response = requests.get(url)
response.raise_for_status()
html = response.text
soup = BeautifulSoup(html, 'html.parser')
tbody = soup.select_one('#container > div.aside > div > div.aside_area.aside_popular > table > tbody')

trs = tbody.select('tr')
datas = []
for tr in trs:
    name = tr.select_one('a').get_text()
    current_price = tr.select_one('td').get_text()
    change_direction = []
    if tr['class'][0] == "up":
        change_direction.append("▲")
    else:
        change_direction.append("▼")
    change_price = tr.select_one('span').get_text()
    datas.append([name, current_price, change_direction, change_price])

# print(datas)
df = pd.DataFrame(datas, columns=['종목명', '현재가', '등락', '전일대비' ], index=range(1, 6))
df = str(df)
print(df)
