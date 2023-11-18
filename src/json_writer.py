from parser import HeadHunter
from filters import filters
import json
from os import chdir


class JsonWriter:

    @staticmethod
    def json_write():
        """

        Метод для записи вакансий в JSON  файл
        """
        # Запрашиваем фильтры
        name, per_page, sort, page_count = filters()

        hh = HeadHunter()

        for i in range(page_count):
            # Преобразуем текст ответа запроса в словарь Python
            full_json = json.loads(hh.parser(name, per_page, sort, i)[0])
            short_json = hh.parser(name, per_page, sort, i)[1]

            # Выводим в консоль полученные результаты в кратком варианте
            print(json.dumps(short_json, indent=2, ensure_ascii=False))

            # Имена файлов JSON для полного и краткого описания вакансий
            # В имени файла содержится фильтр названия вакансии и номер страницы
            long_file_name = f'jsons/long_vacancies_{name if name != "" else "full"}_page_{i + 1}.json'
            short_file_name = f'jsons/short_vacancies_{name if name != "" else "full"}_page_{i + 1}.json'

            chdir('..')

            # Записываем в JSON файлы
            with open(long_file_name, mode='w', encoding='utf8') as js_file:
                js_file.write(json.dumps(full_json, indent=2, ensure_ascii=False))

            with open(short_file_name, mode='w', encoding='utf-8') as js_file:
                js_file.write(json.dumps(short_json, indent=2, ensure_ascii=False))

            if (full_json['pages'] - page_count) <= 1:
                # Проверка на последнюю страницу
                break
