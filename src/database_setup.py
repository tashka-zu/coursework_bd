from typing import Any, Dict

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def create_database(db_name: str) -> None:
    """
    Создает базу данных, если она еще не существует.
    """
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="tasha1502", host="localhost", port="5432")
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")
    cur.close()
    conn.close()


def create_connection(db_name: str) -> psycopg2.extensions.connection:
    """
    Создает и возвращает соединение с базой данных PostgreSQL.
    """
    conn = psycopg2.connect(dbname=db_name, user="postgres", password="tasha1502", host="localhost", port="5432")
    return conn


def create_tables(conn: psycopg2.extensions.connection) -> None:
    """
    Создает таблицы в базе данных.
    """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            salary VARCHAR(100),
            url VARCHAR(255)
        )
        """,
    )
    try:
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
        cursor.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_employer(conn: psycopg2.extensions.connection, employer: Dict[str, Any]) -> None:
    """
    Вставляет данные о работодателе в таблицу employers.
    """
    command: str = """
    INSERT INTO employers (employer_id, name, description, url)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (employer_id) DO NOTHING
    """
    try:
        cursor: psycopg2.extensions.cursor = conn.cursor()
        cursor.execute(
            command, (employer["id"], employer["name"], employer.get("description"), employer.get("alternate_url"))
        )
        cursor.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_vacancy(conn: psycopg2.extensions.connection, vacancy: Dict[str, Any]) -> None:
    """
    Вставляет данные о вакансии в таблицу vacancies.
    """
    command = """
    INSERT INTO vacancies (vacancy_id, name, description, salary, url)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (vacancy_id) DO NOTHING
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            command,
            (
                vacancy["id"],
                vacancy["name"],
                vacancy.get("description"),
                vacancy.get("salary", {}).get("from") if vacancy.get("salary") else None,
                vacancy.get("alternate_url"),
            ),
        )
        cursor.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
