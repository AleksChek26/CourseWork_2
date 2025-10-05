import sys
sys.path.insert(0, '../src')
import os
import unittest
from src.storage import JSONSaver, CSVSaver, XLSSaver
from src.data_models import Vacancy

class TestStorage(unittest.TestCase):
    def tearDown(self):
        files = ["..data/vacancies.json", "..data/vacancies.csv", "..data/vacancies.xlsx"]
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def test_json_saver(self):
        """Тест JSONSaver"""
        saver = JSONSaver()
        vacancy = Vacancy("Developer", "Москва", "https://example.com/dev", 80000, "Fullstack")
        saver.add_vacancy(vacancy)
        saved_data = saver.get_vacancies()
        self.assertIn("Developer", [v['title'] for v in saved_data])
        saver.delete_vacancy(vacancy)
        saved_data = saver.get_vacancies()
        self.assertNotIn("Developer", [v['title'] for v in saved_data])

    def test_csv_saver(self):
        """Тест CSVSaver"""
        saver = CSVSaver()
        vacancy = Vacancy("Designer", "Санкт-Петербург", "https://example.com/design", 70000, "UI/UX Designer")
        saver.add_vacancy(vacancy)
        saved_data = saver.get_vacancies()
        self.assertIn("Designer", [v['title'] for v in saved_data])
        saver.delete_vacancy(vacancy)
        saved_data = saver.get_vacancies()
        self.assertNotIn("Designer", [v['title'] for v in saved_data])

    def test_xls_saver(self):
        """Тест XLSSaver"""
        saver = XLSSaver()
        vacancy = Vacancy("Manager", "Екатеринбург", "https://example.com/manager", 90000, "Project Manager")
        saver.add_vacancy(vacancy)
        saved_data = saver.get_vacancies()
        self.assertIn("Manager", [v['title'] for v in saved_data])
        saver.delete_vacancy(vacancy)
        saved_data = saver.get_vacancies()
        self.assertNotIn("Manager", [v['title'] for v in saved_data])

if __name__ == '__main__':
    unittest.main()