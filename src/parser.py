from abc import ABC, abstractmethod
import requests
import json


class Parser(ABC):

    @abstractmethod
    def parser(self, name, per_page, sort, page_count):
        pass


class HeadHunter(Parser):
    """
    Парсер для HeadHunter
    """

    def parser(self, name, per_page, sort, page_count):
        """

        Получение списка вакансий по фильтрам
        """
        vacancy_name = []
        salary = []
        description = []
        url = []
        company = []
        area = []
        schedule = []

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
        short_data = [{'name': vacancy_name[j], 'salary': salary[j],
                       'description': description[j], 'url': url[j],
                       'area': area[j], 'company': company[j],
                       'schedule': schedule[j]} for j in range(len(vacancy_name))]

        return [data, short_data]
