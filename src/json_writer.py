from HeadHunter import HeadHunter
from SuperJob import SuperJob
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
        sj = SuperJob()
        instances = [hh, sj]
        chdir('..')
        for ins in instances:
            for i in range(page_count):
                # Преобразуем текст ответа запроса в словарь Python
                full_json = json.loads(ins.parser(name, per_page, sort, i)[0])
                short_json = ins.parser(name, per_page, sort, i)[1]

                # Выводим в консоль полученные результаты в кратком варианте
                print(json.dumps(short_json, indent=2, ensure_ascii=False))

                # Имена файлов JSON для полного и краткого описания вакансий
                # В имени файла содержится фильтр названия вакансии и номер страницы
                long_file_name = f'vacancies/long_{ins.__class__.__name__}_vacancies_{name if name != "" else "full"}_page_{i + 1}.json'
                short_file_name = f'vacancies/short_{ins.__class__.__name__}_vacancies_{name if name != "" else "full"}_page_{i + 1}.json'

                # Записываем в JSON файлы
                with open(long_file_name, mode='w', encoding='utf8') as js_file:
                    js_file.write(json.dumps(full_json, indent=2, ensure_ascii=False))

                with open(short_file_name, mode='w', encoding='utf-8') as js_file:
                    js_file.write(json.dumps(short_json, indent=2, ensure_ascii=False))
