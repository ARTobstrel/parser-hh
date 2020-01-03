import requests
from bs4 import BeautifulSoup as bs


headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'}

base_url = 'https://hh.ru/search/vacancy?search_period=3&area=1&text=python&page=0'

jobs = []

def hh_parse(base_url, headers):
    session = requests.Session() #создаем одну сессию. Создаем эмуляцию того что мы ищем вакансию
    request = session.get(base_url, headers=headers)

    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', class_='vacancy-serp-item')
        for div in divs:
            title = div.find('a', class_='bloko-link').text
            href = div.find('a', class_='bloko-link')['href']
            company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            content = f'{text1} {text2}'
            jobs.append({
                'title': title,
                'href': href,
                'company': company,
                'content': content
            })
    else:
        print('ERROR')

if __name__ == '__main__':
    hh_parse(base_url, headers)
    print(jobs)