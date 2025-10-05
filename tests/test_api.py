import sys
sys.path.insert(0, '../src')
import unittest
from src.api import HeadHunterAPI
from requests_mock import mock
import requests

class TestHeadHunterAPI(unittest.TestCase):
    def setUp(self):
        self.api = HeadHunterAPI()

    def test_get_vacancies_success(self):
        """Тест успешного получения вакансий"""
        expected_response = {'items': [
            {'name': 'Python Developer', 'url': 'https://example.com/pd'},
            {'name': 'JavaScript Developer', 'url': 'https://example.com/js'}
        ]}
        with mock() as m:
            m.get("https://api.hh.ru/vacancies", json=expected_response)
            result = self.api.get_vacancies("Python")
            self.assertEqual(result, expected_response['items'])

    def test_get_vacancies_failure(self):
        """Тест неуспешного получения вакансий"""
        with mock() as m:
            m.get("https://api.hh.ru/vacancies", status_code=500)
            with self.assertRaises(requests.exceptions.HTTPError):
                self.api.get_vacancies("Python")

    def test_connect(self):
        """Тест подключения к API (ничего не делает, просто проверяется, что метод существует)"""
        self.api.connect()
        # Так как connect() ничего не делает, достаточно вызвать его без ошибок
