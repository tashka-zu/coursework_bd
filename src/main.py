from api_handler import get_employers, get_vacancies
from database_setup import create_connection, create_tables, insert_employer, insert_vacancy
from user_interface import main as user_interface_main

def load_data_to_database():
    """Загружает данные о работодателях и вакансиях в базу данных."""
    # Пример списка идентификаторов работодателей
    employer_ids = [1740, 78638, 3529, 10965, 15478, 907345, 3779, 1455, 4181, 2345]

    # Получение данных о работодателях и вакансиях
    employers = get_employers(employer_ids)

    # Подключение к базе данных
    conn = create_connection()
    create_tables(conn)

    # Вставка данных о работодателях и вакансиях в базу данных
    for employer in employers:
        insert_employer(conn, employer)
        vacancies = get_vacancies(employer['id'])
        for vacancy in vacancies:
            insert_vacancy(conn, vacancy)

    # Закрытие соединения с базой данных
    conn.close()

def main():
    """Основная функция для запуска программы."""
    # Загрузка данных в базу данных
    load_data_to_database()

    # Запуск интерфейса пользователя
    user_interface_main()

if __name__ == "__main__":
    main()
