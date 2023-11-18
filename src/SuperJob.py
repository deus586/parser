import requests
from parser import Parser
import json
import os

sj_API_KEY = os.environ['SUPERJOB_API_KEY']


class SuperJob(Parser):
    def __init__(self):
        self.headers = {
            'X-Api-App-Id': sj_API_KEY
        }

    def parser(self, name: str, per_page: int, sort: int, page_count: int) -> list:
        """

        Получение списка вакансий по фильтрам с сайта SuperJob
        """
        vacancy_name = []
        salary = []
        description = []
        url = []
        company = []
        area = []
        schedule = []

        sort_variable = {1: 'relevance', 2: 'payment_sort%5D=asc',
                         3: 'payment_sort%5D=desc', 4: 'date'}

        sort = sort_variable[sort]

        params = {
            'keyword': name,
            'count': per_page,
            'page': page_count,
            'order_field': sort
        }

        response = requests.get('https://api.superjob.ru/2.0/vacancies', headers=self.headers, params=params).json()

        for i in response['objects']:
            schedule.append(i['type_of_work']['title'])
            area.append(i['town']['title'])
            try:
                company.append(i['firm_name'])
            except TypeError:
                company.append('Компания не указана.')
            url.append(i['link'])
            vacancy_name.append(i['profession'])
            if i['firm_activity'] is not None:
                description.append(i['firm_activity'])
            else:
                description.append('Описание не указано.')

            if i['payment_to'] != 0:
                salary.append({'from': 'от ' + str(i['payment_from']) + f' {i["currency"]}',
                               'to': 'до ' + str(i['payment_to']) + f' {i["currency"]}'})
            else:
                salary.append({'from': 'от ' + str(i['payment_from']) + f' {i["currency"]}'})

        # Составляем словарь с краткой информацией
        short_data = self.short_data(vacancy_name, salary, description, url, area, company, schedule)

        return [json.dumps(response), short_data]

    def short_data(self, vacancy_name: list, salary: list, description: list, url: list, area: list, company: list, schedule: list) -> list:
        return super().short_data(vacancy_name, salary, description, url, area, company, schedule)
