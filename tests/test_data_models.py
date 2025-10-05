import sys
sys.path.insert(0, '../src')
import unittest
from src.data_models import Vacancy

class TestVacancy(unittest.TestCase):
    def setUp(self):
        # Добавляем город в конструкторе
        self.valid_vacancy = Vacancy("Software Engineer", "Санкт-Петербург", "https://example.com/se", 100000, "Требуются знания Python и Django")
        self.invalid_vacancy = Vacancy("Invalid Job", "Москва", "invalid-link", -10000, "Description here")

    def test_valid_vacancy(self):
        """Проверка корректной вакансии"""
        self.valid_vacancy.validate()

    def test_invalid_vacancy(self):
        """Проверка некорректной вакансии"""
        with self.assertRaises(ValueError):
            self.invalid_vacancy.validate()

    def test_cast_to_object_list(self):
        """Преобразование JSON-списка в список объектов Vacancy"""
        raw_data = [
            {"name": "Python Developer", "url": "https://example.com/pd", "salary": {"to": 80000}, "snippet": {"requirement": "Опыт от 3 лет"}, "area": {"name": "Москва"}},
            {"name": "Senior JavaScript Developer", "url": "https://example.com/jsd", "salary": {"to": 120000}, "snippet": {"requirement": "React.js"}, "area": {"name": "Санкт-Петербург"}},
            {"name": "Incomplete Entry", "url": "https://example.com/incomplete"}  # Недостающие поля
        ]
        vacancies = Vacancy.cast_to_object_list(raw_data)
        self.assertGreater(len(vacancies), 0)  # Должно быть хотя бы две вакансии
        self.assertIsInstance(vacancies[0], Vacancy)
        self.assertEqual(vacancies[0].title, "Python Developer")
        self.assertEqual(vacancies[0].city, "Москва")  # Проверяем наличие города

if __name__ == '__main__':
    unittest.main()
