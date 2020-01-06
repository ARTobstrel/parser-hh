import requests
import csv
from bs4 import BeautifulSoup as bs

#Напишите любую вакансию
vacancy = 'python'

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'}

base_url = f'https://hh.ru/search/vacancy?search_period=3&area=1&text={vacancy}к&page=0'

jobs = []
urls = []
urls.append(base_url)

def hh_parse(base_url, headers):
    session = requests.Session() #создаем одну сессию. Создаем эмуляцию того что мы ищем вакансию
    request = session.get(base_url, headers=headers)

    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://hh.ru/search/vacancy?search_period=3&area=1&text={vacancy}&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
        for url in urls:
            request = session.get(url, headers=headers)
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
            print(len(jobs))
    else:
        print('ERROR')

    return jobs

def files_writer(jobs):
    with open('parsed_jobs.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow({'Вакансия', 'URL', 'Компания', 'Описание'})
        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['company'], job['content']))

if __name__ == '__main__':
    jobs = hh_parse(base_url, headers)
    files_writer(jobs)