from db_manager import DBManager


def display_menu() -> None:
    """Отображает меню для взаимодействия с пользователем."""
    print("\nВыберите действие:")
    print("1. Получить список всех вакансий")
    print("2. Получить среднюю зарплату по вакансиям")
    print("3. Получить список вакансий с зарплатой выше средней")
    print("4. Получить список вакансий по ключевому слову")
    print("5. Выход")


def get_all_vacancies(db_manager: DBManager) -> None:
    """Получает и отображает список всех вакансий."""
    vacancies = db_manager.get_all_vacancies()
    for vacancy in vacancies:
        print(f"Вакансия: {vacancy[0]}, Зарплата: {vacancy[1]}, Ссылка: {vacancy[2]}")


def get_avg_salary(db_manager: DBManager) -> None:
    """Получает и отображает среднюю зарплату по вакансиям."""
    avg_salary = db_manager.get_avg_salary()
    print(f"Средняя зарплата по вакансиям: {avg_salary}")


def get_vacancies_with_higher_salary(db_manager: DBManager) -> None:
    """Получает и отображает список вакансий с зарплатой выше средней."""
    vacancies = db_manager.get_vacancies_with_higher_salary()
    for vacancy in vacancies:
        print(f"Вакансия: {vacancy[0]}, Зарплата: {vacancy[1]}, Ссылка: {vacancy[2]}")


def get_vacancies_with_keyword(db_manager: DBManager) -> None:
    """Получает и отображает список вакансий по ключевому слову."""
    keyword = input("Введите ключевое слово для поиска вакансий: ")
    vacancies = db_manager.get_vacancies_with_keyword(keyword)
    for vacancy in vacancies:
        print(f"Вакансия: {vacancy[0]}, Зарплата: {vacancy[1]}, Ссылка: {vacancy[2]}")


def user_interface_main() -> None:
    """Основная функция для взаимодействия с пользователем."""
    db_manager = DBManager()
    try:
        while True:
            display_menu()
            choice = input("Введите номер действия: ")
            if choice == "1":
                get_all_vacancies(db_manager)
            elif choice == "2":
                get_avg_salary(db_manager)
            elif choice == "3":
                get_vacancies_with_higher_salary(db_manager)
            elif choice == "4":
                get_vacancies_with_keyword(db_manager)
            elif choice == "5":
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Пожалуйста, попробуйте снова.")
    finally:
        db_manager.close()
