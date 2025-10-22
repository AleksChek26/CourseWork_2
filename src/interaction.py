from api import HeadHunterAPI
from data_models import Vacancy
from storage import JSONSaver, CSVSaver, XLSSaver


class UserInteraction:
    """Обеспечивает взаимодействие с пользователем через консоль"""

    def run(self):
        hh_api = HeadHunterAPI()
        profession = input("🧐 Введите желаемую профессию (например, 'Java-разработчик'): ")
        vacancies = hh_api.get_vacancies(profession)
        vacancies_objs = Vacancy.cast_to_object_list(vacancies)

        saver = JSONSaver()  # или CSVSaver(), или XLSSaver()
        for vacancy in vacancies_objs:
            saver.add_vacancy(vacancy)

        while True:
            print("\n🔍 Меню:")
            print("1️⃣ Показать вакансии")
            print("2️⃣ Выбрать вакансию")
            print("3️⃣ Фильтрация по зарплате")
            print("4️⃣ Фильтрация по региону")
            print("5️⃣ Фильтрация по опыту работы")
            print("6️⃣ Фильтрация по городу")
            print("7️⃣ Удалить вакансию")
            print("8️⃣ Перезадать профессию")
            print("9️⃣ Выход")
            choice = input("✨ Ваш выбор: ")

            if choice == '1':
                self.show_vacancies(saver.get_vacancies())

            elif choice == '2':
                self.select_vacancy(saver.get_vacancies())

            elif choice == '3':
                min_salary = input("💰 Минимальная зарплата: ")
                max_salary = input("💰 Максимальная зарплата: ")
                filtered = saver.get_vacancies({"salary": (float(min_salary), float(max_salary))})
                self.show_vacancies(filtered)

            elif choice == '4':
                region = input("🏘 Регион (Москва, Петербург и т.д.): ")
                filtered = saver.get_vacancies({"region": region})
                self.show_vacancies(filtered)

            elif choice == '5':
                exp_level = input("👩‍💻 Уровень опыта (Junior/Middle/Senior): ")
                filtered = saver.get_vacancies({"experience": exp_level})
                self.show_vacancies(filtered)

            elif choice == '6':  # Фильтрация по городу
                city = input("📍 Город (например, Москва): ")
                filtered = saver.get_vacancies({"city": city})
                self.show_vacancies(filtered)

            elif choice == '7':
                title = input("📌 Название вакансии для удаления: ")
                link = input("🔗 Ссылка на вакансию: ")
                vacancy_to_delete = Vacancy(title, '', link, None, '')
                saver.delete_vacancy(vacancy_to_delete)
                print("✅ Удалено!")

            elif choice == '8':
                profession = input("🧐 Введите новую профессию (например, 'Android-разработчик'): ")
                vacancies = hh_api.get_vacancies(profession)
                vacancies_objs = Vacancy.cast_to_object_list(vacancies)
                saver.clear()  # очищаем старое хранилище
                for vacancy in vacancies_objs:
                    saver.add_vacancy(vacancy)

            elif choice == '9':
                break

            else:
                print("❗ Ошибка выбора меню. Повторите попытку.")

    def select_vacancy(self, vacancies):
        if len(vacancies) == 0:
            print("🚫 Нет подходящих вакансий.")
            return

        print("\nСписок вакансий:\n")
        for idx, vacancy in enumerate(vacancies):
            print(
                f"{idx + 1}. 🎯 {vacancy['title']} ({vacancy['city']}) 👉 {vacancy['link']}\nЗаработок: {vacancy['salary']}\nОписание: {vacancy['description']}\n")

        selection = input("🖊 Выберите номер вакансии для детализации (или Enter для отмены): ")
        if selection.isdigit() and 1 <= int(selection) <= len(vacancies):
            selected_idx = int(selection) - 1
            selected_vacancy = vacancies[selected_idx]
            print("\nПодробная информация о вакансии:\n")
            print(f"🎯 Название: {selected_vacancy['title']}")
            print(f"📍 Город: {selected_vacancy['city']}")  # Добавлен вывод города
            print(f"🔗 Ссылка: {selected_vacancy['link']}")
            print(f"💰 Заработок: {selected_vacancy['salary']}")
            print(f"📝 Требования: {selected_vacancy['description']}")
        else:
            print("❌ Отмена выбора.")

    def show_vacancies(self, vacancies):
        if len(vacancies) > 0:
            for i, vacancy in enumerate(vacancies):
                print(
                    f"\n{i + 1}. 🎯 {vacancy['title']} ({vacancy['city']}) 👉 {vacancy['link']}\nЗаработок: {vacancy['salary']}\nОписание: {vacancy['description']}")
        else:
            print("🚫 Нет подходящих вакансий.")
