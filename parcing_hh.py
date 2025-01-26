"""
Парсер для hh.ru основываясь на API.
Парсит по 6 вакансий.
Для изменения профессии надо менять api.
"""

import requests
from bs4 import BeautifulSoup
import re

def slice_line(element):
    return f'{element[:300]}...' if len(element) > 300 else element

def get_vacancies():
    url = "https://api.hh.ru/widgets/vacancies/search?count=6&locale=RU&links_color=1560b2&border_color=1560b2&text=python-%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82"

    exchange = {
        '₽': 1.0,
        '$': 100.0,
        '€': 105.0,
        '₸': 0.210,
        'Br': 30.0,
    }


    response = requests.get(url)
    html = BeautifulSoup(response.text, "html.parser")
    film = html.find_all("a",  class_="hh-vacancy__link-css_class_postfix")

    pattern = r'href="(https://[^"]+)"'
    k = []
    link_list = []
    for i in film:
        match = re.search(pattern, str(i))
        link = match.group(1)
        link_list.append(link)
        k.append(i)
    kon_mas = []
    
    for j in range(len(link_list)):
        job_list = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive'
        }
        slim = link_list[j]
        response2 = requests.get(slim, headers=headers)
        html2 = BeautifulSoup(response2.text, 'html.parser')

        title = html2.find('h1', {'data-qa': 'title'}) #название вакансии
        if title:
            job_list.append(title.text.strip())
        else:
            job_list.append('Не указано')

        description_element = html2.find("div", class_="g-user-content") #описание вакансии
        if description_element:
            job_list.append(slice_line(str(description_element.text.strip())))
        else:
            job_list.append('Не указано')

        skills_elements = html2.find_all("div", class_="magritte-tag__label___YHV-o_3-0-25") #навыки
        skills_list = [skill.text for skill in skills_elements]
        if skills_list:
            skills_list.pop(-1)
            job_list.append(skills_list)
        else:
            job_list.append('Не указано')

        company_element = html2.find("span", class_="vacancy-company-name") #название компании
        if company_element:
            job_list.append(company_element.text.replace('\xa0', ' '))
        else:
            job_list.append('Не указано')

        salary_element = html2.find("div", attrs={"data-qa": "vacancy-salary"}) #деньги
        if salary_element:
            span_element = salary_element.find("span")
            if span_element:
                money = []
                currency = 0
                for child in span_element.children:
                    if exchange.get(child):
                        currency = exchange.get(child)
                    if str(child)[0].isnumeric():
                        money.append(child.replace("\xa0", ""))
                job_list.append(f"{float(money[0]) * currency} - {float(money[1]) * currency}" if len(
                    money) > 1 else f"{float(money[0]) * currency}")
        else:
            job_list.append('Не указано')

        address_html = html2.find("span", attrs={"data-qa": "vacancy-view-raw-address"}) #адрес вакансии
        if address_html:
            job_list.append(address_html.text)
        else:
            job_list.append('Не указано')

        address_html = html2.find("p", class_="vacancy-creation-time-redesigned") #дата публикации вакансии
        if address_html:
            job_list.append(address_html.find('span').text.replace('\xa0', ' '))
        else:
            job_list.append('Не указано')

        kon_mas.append(job_list)
    return kon_mas

print(get_vacancies())