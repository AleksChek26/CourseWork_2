import os
import json
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, List
from .data_models import Vacancy

class AbstractDataSaver(ABC):
    """Абстрактный класс для хранения вакансий"""
    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, criteria=None):
        pass


class JSONSaver(AbstractDataSaver):
    """Реализует хранение вакансий в JSON-файлах"""
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(current_dir, '..', 'data', 'vacancies.json')

    def add_vacancy(self, vacancy: Vacancy):
        existing_data = self._load_json()
        new_entry = {
            "title": vacancy.title,
            "city": vacancy.city,              # Новое поле
            "link": vacancy.link,
            "salary": vacancy.salary,
            "description": vacancy.description
        }
        existing_data.append(new_entry)
        self._save_json(existing_data)

    def _load_json(self) -> List[Dict]:
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _save_json(self, data: List[Dict]):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def delete_vacancy(self, vacancy: Vacancy):
        data = self._load_json()
        updated_data = [
            entry for entry in data
            if entry["title"] != vacancy.title or entry["link"] != vacancy.link
        ]
        self._save_json(updated_data)

    def get_vacancies(self, criteria=None) -> List[Dict]:
        data = self._load_json()
        if criteria:
            result = []
            for entry in data:
                matches_criteria = True
                for key, value in criteria.items():
                    if isinstance(value, tuple):  # Критерии диапазона (зарплаты)
                        low, high = value
                        if not (low <= entry.get(key, 0) <= high):
                            matches_criteria = False
                            break
                    elif entry.get(key) != value:
                        matches_criteria = False
                        break
                if matches_criteria:
                    result.append(entry)
            return result
        return data


class CSVSaver(AbstractDataSaver):
    """Реализует хранение вакансий в CSV-файлах"""
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(current_dir, '..', 'data', 'vacancies.csv')

    def add_vacancy(self, vacancy: Vacancy):
        df = self._load_csv()
        new_row = pd.DataFrame({
            "title": [vacancy.title],
            "city": [vacancy.city],              # Новое поле
            "link": [vacancy.link],
            "salary": [vacancy.salary],
            "description": [vacancy.description]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        self._save_csv(df)

    def _load_csv(self) -> pd.DataFrame:
        try:
            return pd.read_csv(self.filename)
        except FileNotFoundError:
            return pd.DataFrame(columns=["title", "city", "link", "salary", "description"])

    def _save_csv(self, df: pd.DataFrame):
        df.to_csv(self.filename, index=False)

    def delete_vacancy(self, vacancy: Vacancy):
        df = self._load_csv()
        df = df[(df["title"] != vacancy.title) & (df["link"] != vacancy.link)]
        self._save_csv(df)

    def get_vacancies(self, criteria=None) -> List[Dict]:
        df = self._load_csv()
        if criteria:
            df = df.query(" & ".join([f"`{key}`=='{value}'" for key, value in criteria.items()]))
        return df.to_dict(orient="records")


class XLSSaver(AbstractDataSaver):
    """Реализует хранение вакансий в XLSX-файлах"""
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(current_dir, '..', 'data', 'vacancies.xlsx')

    def add_vacancy(self, vacancy: Vacancy):
        df = self._load_xlsx()
        new_row = pd.DataFrame({
            "title": [vacancy.title],
            "city": [vacancy.city],              # Новое поле
            "link": [vacancy.link],
            "salary": [vacancy.salary],
            "description": [vacancy.description]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        self._save_xlsx(df)

    def _load_xlsx(self) -> pd.DataFrame:
        try:
            return pd.read_excel(self.filename)
        except FileNotFoundError:
            return pd.DataFrame(columns=["title", "city", "link", "salary", "description"])

    def _save_xlsx(self, df: pd.DataFrame):
        df.to_excel(self.filename, index=False)

    def delete_vacancy(self, vacancy: Vacancy):
        df = self._load_xlsx()
        df = df[(df["title"] != vacancy.title) & (df["link"] != vacancy.link)]
        self._save_xlsx(df)

    def get_vacancies(self, criteria=None) -> List[Dict]:
        df = self._load_xlsx()
        if criteria:
            df = df.query(" & ".join([f"`{key}`=='{value}'" for key, value in criteria.items()]))
        return df.to_dict(orient="records")
