#с января 2003 по декабрь 2024
import re
import requests
from bs4 import BeautifulSoup
import json


def remove_html_tags(text):
    return re.sub(r'<[^>]+>', '', text)
base_dict = {}
month_dict = {}
for i in range(22):
    for j in range(1, 13):
        if len(str(j)) == 1:
            k = str(f'0{j}')
        else:
            k = j
        url = f'https://cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To=01.{k}.{2003 + i}'
        fin = requests.get(url)
        html = BeautifulSoup(fin.text, "html.parser")
        film = html.find_all("div",  class_="table")
        film1 = html.find_all("td")
        year_dict = {}
        for k in range(1, len(film1), 5):
            text = remove_html_tags(str(film1[k]))
            text1 = remove_html_tags(str(film1[k + 3]))
            year_dict[text] = text1
        month_dict[str(j) + '_' + str(2003 + i)] = year_dict
    # base_dict[2003 + i] = month_dict
sim = json.dumps(month_dict)
with open('fign.txt', 'w') as f:
    f.write(sim)
