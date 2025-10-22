from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Vacancy:
    """Модель вакансии"""
    title: str               # Название вакансии
    city: str                # Город размещения вакансии
    link: str                # Ссылка на вакансию
    salary: Optional[int]    # Зарплата (может отсутствовать)
    description: str         # Краткое описание или требования

    def _validate(self):
        """
        Приватный метод для валидации объекта вакансии.
        """
        if self.salary is not None and self.salary <= 0:
            raise ValueError(f"Некорректная зарплата {self.salary}")

    def __lt__(self, other):
        """Метод для сравнения двух вакансий по зарплате (<)"""
        if self.salary is None:
            return False
        if other.salary is None:
            return True
        return self.salary < other.salary

    def __gt__(self, other):
        """Метод для сравнения двух вакансий по зарплате (>)"""
        if self.salary is None:
            return False
        if other.salary is None:
            return True
        return self.salary > other.salary

    @staticmethod
    def cast_to_object_list(data: List[dict]) -> List['Vacancy']:
        """
        Преобразует список JSON-данных в список объектов Vacancy.
        Пропускает записи с ошибочными значениями.
        """
        vacancies = []
        for item in data:
            try:
                # Проверяем наличие необходимых полей
                if 'name' not in item or 'url' not in item or 'snippet' not in item:
                    continue  # пропускаем вакансию, если обязательные поля отсутствуют

                # Получаем зарплату, обрабатывая возможное отсутствие минимальной/максимальной зарплаты
                salary = item['salary']['to'] if item['salary'] else None

                # Новый пункт: получаем город вакансии
                city = item['area']['name'] if 'area' in item else ''

                vacancy = Vacancy(
                    title=item['name'],      # название вакансии
                    city=city,               # город вакансии
                    link=item['url'],        # ссылка на вакансию
                    salary=salary,           # максимальная зарплата
                    description=item['snippet'].get('requirement', '')  # описание вакансии
                )
                vacancy._validate()
                vacancies.append(vacancy)
            except Exception as e:
                print(f"Пропущена некорректная запись: {e}")
        return vacancies
