import requests
from abc import ABC, abstractmethod

class AbstractJobPlatformAPI(ABC):
    """Абстрактный класс для работы с API платформ вакансий"""
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_vacancies(self, query: str):
        pass


class HeadHunterAPI(AbstractJobPlatformAPI):
    """Конкретная реализация API HeadHunter"""
    BASE_URL = "https://api.hh.ru"

    def connect(self):
        # Подключение к API осуществляется непосредственно при запросе
        pass

    def get_vacancies(self, query: str):
        """
        Возвращает список вакансий по указанному запросу.
        :param query: строка поиска (например, профессия)
        :return: словарь с результатами
        """
        response = requests.get(f"{self.BASE_URL}/vacancies",
                               params={"text": query, "per_page": 10})
        response.raise_for_status()
        return response.json()['items']
