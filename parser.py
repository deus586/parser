from abc import ABC, abstractmethod
import requests
import json


class Parser(ABC):

    @abstractmethod
    def parser(self, name, per_page, sort, page_count):
        pass


class HeadHunter(Parser):

    def parser(self, name, per_page, sort, page_count):
        vacancy_name = []
        salary = []
        description = []
        url = []
        company = []
        area = []
        schedule = []

        params = {
            'text': name,
            'page': page_count,  # Индекс страницы поиска на HH
            'per_page': per_page,  # Кол-во вакансий на 1 странице
            'order_by': sort
        }

        req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
        data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()

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

        short_data = [{'name': vacancy_name[j], 'salary': salary[j],
                       'description': description[j], 'url': url[j],
                       'area': area[j], 'company': company[j],
                       'schedule': schedule[j]} for j in range(len(vacancy_name))]

        return [data, short_data]


class JsonWriter:

    @staticmethod
    def json_write():
        name, per_page, sort, page_count = filters()
        hh = HeadHunter()
        for i in range(page_count):
            # Преобразуем текст ответа запроса в справочник Python
            full_json = json.loads(hh.parser(name, per_page, sort, i)[0])
            short_json = hh.parser(name, per_page, sort, i)[1]
            print(json.dumps(short_json, indent=2, ensure_ascii=False))
            long_file_name = f'long_vacancies_{name if name != "" else "full"}_page_{i + 1}.json'
            short_file_name = f'short_vacancies_{name if name != "" else "full"}_page_{i + 1}.json'

            with open(long_file_name, mode='w', encoding='utf8') as js_file:
                js_file.write(json.dumps(full_json, indent=2, ensure_ascii=False))

            with open(short_file_name, mode='w', encoding='utf-8') as js_file:
                js_file.write(json.dumps(short_json, indent=2, ensure_ascii=False))

            if (full_json['pages'] - page_count) <= 1:
                break


def filters():
    name = ''
    per_page = 100
    sort = 'relevance'
    page_count = 1
    sort_variable = {1: 'relevance', 2: 'salary_asc',
                     3: 'salary_desc', 4: 'publication_time'}
    user_input = input('Хотите ли ввести фильтры?(Y/N): ')
    while True:
        if user_input.upper() == 'N':
            break
        elif user_input.upper() == 'Y':
            print('Какие фильтры хотите ввести:')
            print('1. Название вакансии')
            print('2. Количество вакансий(по умолчанию: 100)')
            print('3. Варианты сортировки(по умолчанию: по соответствию)')
            print('4. Количество страниц(по умолчанию: 1)')
            choose = int(input())

            if choose == 1:
                name = input('Введите название: ')
            elif choose == 2:
                try:
                    per_page = int(input('Введите количество вакансий(не больше 100): '))
                except ValueError:
                    print('Неверный тип данных.')
                if per_page > 100:
                    print('Слишком много вакансий на одну страницу.')
                    per_page = 100
            elif choose == 3:
                print("1. По соответствию\n2. По возрастанию оплаты\n3. По убыванию оплаты\n4. По дате")
                sort = input('Введите вариант сортировки: ')
                try:
                    sort = sort_variable[int(sort)]
                except KeyError:
                    print('Нет такого варианта.')
            elif choose == 4:
                try:
                    page_count = int(input('Введите количество страниц: '))
                except ValueError:
                    print('Неверный тип данных.')
            else:
                print('Нет такого варианта.')

        user_input = input('Хотите продолжить?(Y/N): ')
    return [name, per_page, sort, page_count]


# JsonWriter().json_write()
