import requests

from database_setup import create_connection, create_database, create_tables, insert_employer, insert_vacancy
from user_interface import user_interface_main


def get_employers_and_vacancies():
    """Получает данные о работодателях и вакансиях с hh.ru."""
    url = "https://api.hh.ru/vacancies"
    params = {"per_page": 100}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["items"]
    return []


def load_data_to_database(conn):
    """Загружает данные о вакансиях и работодателях в базу данных."""
    vacancies = get_employers_and_vacancies()

    for vacancy in vacancies:
        employer = vacancy.get("employer")
        if employer:
            insert_employer(conn, employer)
        insert_vacancy(conn, vacancy)


def main():
    """Основная функция для запуска программы."""
    db_name = "hh_data"
    create_database(db_name)
    conn = create_connection(db_name)
    if conn:
        try:
            create_tables(conn)
            load_data_to_database(conn)
        finally:
            conn.close()
        user_interface_main()


if __name__ == "__main__":
    main()
