from abc import ABC, abstractmethod


class Parser(ABC):

    @abstractmethod
    def parser(self, name: str, per_page: int, sort: int, page_count: int):
        pass

    @abstractmethod
    def short_data(self, vacancy_name: list, salary: list, description: list, url: list, area: list, company: list, schedule: list) -> list:
        short_data = [{'name': vacancy_name[j], 'salary': salary[j],
                       'description': description[j], 'url': url[j],
                       'area': area[j], 'company': company[j],
                       'schedule': schedule[j]} for j in range(len(vacancy_name))]
        return short_data
