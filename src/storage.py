import os
import json
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, List
from src.data_models import Vacancy

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
    DATA_DIR = "data"  # Папка для хранения данных

    def __init__(self, filename="vacancies.json"):
        # Проверяем существование папки и создаем её, если её нет
        os.makedirs(JSONSaver.DATA_DIR, exist_ok=True)
        self.file_path = os.path.join(JSONSaver.DATA_DIR, filename)

    def add_vacancy(self, vacancy: Vacancy):
        existing_data = self._load_json()
        new_entry = {
            "title": vacancy.title,
            "city": vacancy.city,
            "link": vacancy.link,
            "salary": vacancy.salary,
            "description": vacancy.description
        }
        existing_data.append(new_entry)
        self._save_json(existing_data)

    def _load_json(self) -> List[Dict]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _save_json(self, data: List[Dict]):
        with open(self.file_path, 'w', encoding='utf-8') as file:
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
                        current_salary = entry.get(key)
                        if current_salary is None or not (low <= current_salary <= high):
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
    DATA_DIR = "data"  # Папка для хранения данных

    def __init__(self, filename="vacancies.csv"):
        # Проверяем существование папки и создаем её, если её нет
        os.makedirs(CSVSaver.DATA_DIR, exist_ok=True)
        self.file_path = os.path.join(CSVSaver.DATA_DIR, filename)

    def add_vacancy(self, vacancy: Vacancy):
        df = self._load_csv()
        new_row = pd.DataFrame({
            "title": [vacancy.title],
            "city": [vacancy.city],
            "link": [vacancy.link],
            "salary": [vacancy.salary],
            "description": [vacancy.description]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        self._save_csv(df)

    def _load_csv(self) -> pd.DataFrame:
        try:
            return pd.read_csv(self.file_path)
        except FileNotFoundError:
            return pd.DataFrame(columns=["title", "city", "link", "salary", "description"])

    def _save_csv(self, df: pd.DataFrame):
        df.to_csv(self.file_path, index=False)

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
    DATA_DIR = "data"  # Папка для хранения данных

    def __init__(self, filename="vacancies.xlsx"):
        # Проверяем существование папки и создаем её, если её нет
        os.makedirs(XLSSaver.DATA_DIR, exist_ok=True)
        self.file_path = os.path.join(XLSSaver.DATA_DIR, filename)

    def add_vacancy(self, vacancy: Vacancy):
        df = self._load_xlsx()
        new_row = pd.DataFrame({
            "title": [vacancy.title],
            "city": [vacancy.city],
            "link": [vacancy.link],
            "salary": [vacancy.salary],
            "description": [vacancy.description]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        self._save_xlsx(df)

    def _load_xlsx(self) -> pd.DataFrame:
        try:
            return pd.read_excel(self.file_path)
        except FileNotFoundError:
            return pd.DataFrame(columns=["title", "city", "link", "salary", "description"])

    def _save_xlsx(self, df: pd.DataFrame):
        df.to_excel(self.file_path, index=False)

    def delete_vacancy(self, vacancy: Vacancy):
        df = self._load_xlsx()
        df = df[(df["title"] != vacancy.title) & (df["link"] != vacancy.link)]
        self._save_xlsx(df)

    def get_vacancies(self, criteria=None) -> List[Dict]:
        df = self._load_xlsx()
        if criteria:
            df = df.query(" & ".join([f"`{key}`=='{value}'" for key, value in criteria.items()]))
        return df.to_dict(orient="records")
