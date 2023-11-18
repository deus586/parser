import requests
import json
from parser import Parser


class HeadHunter(Parser):
    """
    Парсер для HeadHunter
    """

    def parser(self, name: str, per_page: int, sort: int, page_count: int) -> list:
        """

        Получение списка вакансий по фильтрам с сайта HeadHunter
        """
        vacancy_name = []
        salary = []
        description = []
        url = []
        company = []
        area = []
        schedule = []

        sort_variable = {1: 'relevance', 2: 'salary_asc',
                         3: 'salary_desc', 4: 'publication_time'}

        sort = sort_variable[sort]

        # Фильтры
        params = {
            'text': name,
            'page': page_count,
            'per_page': per_page,
            'order_by': sort
        }
        # Посылаем запрос к API
        req = requests.get('https://api.hh.ru/vacancies', params)
        # Декодируем его ответ, чтобы Кириллица отображалась корректно
        data = req.content.decode()
        req.close()

        # Записываем отдельные данные для получения краткой информации по вакансиям
        for i in json.loads(data)['items']:
            schedule.append(i['schedule']['name'])
            area.append(i['area']['name'])
            try:
                company.append(i['department']['name'])
            except TypeError:
                company.append('Компания не указана.')
            url.append(i['alternate_url'])
            vacancy_name.append(i['name'])
            if i['snippet']['responsibility'] is not None:
                description.append(i['snippet']['responsibility'])
            else:
                description.append('Описание не указано.')
            if i['salary'] is not None:
                if i['salary']['from'] is not None:
                    salary.append('от ' + str(i['salary']['from']) + f' {i["salary"]["currency"]}')
                else:
                    salary.append('до ' + str(i['salary']['to']) + f' {i["salary"]["currency"]}')
            else:
                salary.append('Не указано.')

        # Составляем словарь с краткой информацией
        short_data = self.short_data(vacancy_name, salary, description, url, area, company, schedule)

        return [data, short_data]

    def short_data(self, vacancy_name: list, salary: list, description: list, url: list, area: list, company: list, schedule: list) -> list:
        return super().short_data(vacancy_name, salary, description, url, area, company, schedule)
