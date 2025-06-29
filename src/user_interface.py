from db_manager import DBManager


def display_menu() -> None:
    """Отображает меню для взаимодействия с пользователем"""
    print("\nВыберите действие:")
    print("1. Получить список всех компаний и количество вакансий у каждой компании")
    print("2. Получить список всех вакансий")
    print("3. Получить среднюю зарплату по вакансиям")
    print("4. Получить список вакансий с зарплатой выше средней")
    print("5. Получить список вакансий по ключевому слову")
    print("6. Выход")


def get_companies_and_vacancies_count(db_manager: DBManager) -> None:
    """Получает и отображает список всех компаний и количество вакансий у каждой компании"""
    companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
    for company, count in companies_and_vacancies:
        print(f"Компания: {company}, Количество вакансий: {count}")


def get_all_vacancies(db_manager: DBManager) -> None:
    """Получает и отображает список всех вакансий"""
    vacancies = db_manager.get_all_vacancies()
    for vacancy in vacancies:
        print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, Ссылка: {vacancy[3]}")


def get_avg_salary(db_manager: DBManager) -> None:
    """Получает и отображает среднюю зарплату по вакансиям"""
    avg_salary = db_manager.get_avg_salary()
    print(f"Средняя зарплата по вакансиям: {avg_salary}")


def get_vacancies_with_higher_salary(db_manager: DBManager) -> None:
    """Получает и отображает список вакансий с зарплатой выше средней"""
    vacancies = db_manager.get_vacancies_with_higher_salary()
    for vacancy in vacancies:
        print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, Ссылка: {vacancy[3]}")


def get_vacancies_with_keyword(db_manager: DBManager) -> None:
    """Получает и отображает список вакансий по ключевому слову"""
    keyword = input("Введите ключевое слово для поиска вакансий: ")
    vacancies = db_manager.get_vacancies_with_keyword(keyword)
    for vacancy in vacancies:
        print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, Ссылка: {vacancy[3]}")


def main() -> None:
    db_manager = DBManager()
    while True:
        display_menu()
        choice = input("Введите номер действия: ")
        if choice == "1":
            get_companies_and_vacancies_count(db_manager)
        elif choice == "2":
            get_all_vacancies(db_manager)
        elif choice == "3":
            get_avg_salary(db_manager)
        elif choice == "4":
            get_vacancies_with_higher_salary(db_manager)
        elif choice == "5":
            get_vacancies_with_keyword(db_manager)
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")
