import psycopg2

from api_handler import get_vacancies
from database_setup import create_connection, create_database, create_tables, insert_vacancy
from user_interface import user_interface_main


def load_data_to_database(conn: psycopg2.extensions.connection) -> None:
    """
    Загружает данные о вакансиях в базу данных.
    """
    vacancies = get_vacancies(per_page=100)
    print(f"Найдено вакансий: {len(vacancies)}")

    for vacancy in vacancies:
        print(f"Добавление вакансии: {vacancy['name']}")
        insert_vacancy(conn, vacancy)


def main() -> None:
    """Основная функция для запуска программы."""
    db_name = "hh_data"
    create_database(db_name)
    conn = create_connection(db_name)
    if conn:
        create_tables(conn)
        load_data_to_database(conn)
        conn.close()

        user_interface_main()


if __name__ == "__main__":
    main()
