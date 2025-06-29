import os
from typing import Any, Dict

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def create_connection() -> psycopg2.extensions.connection:
    """Создает и возвращает соединение с базой данных PostgreSQL."""
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    return conn


def create_tables(conn: psycopg2.extensions.connection) -> None:
    """Создает таблицы в базе данных."""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS employers (
            employer_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            url VARCHAR(255)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            employer_id INTEGER REFERENCES employers(employer_id),
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
    """Вставляет данные о работодателе в таблицу employers."""
    command = """
    INSERT INTO employers (employer_id, name, description, url)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (employer_id) DO NOTHING
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            command, (employer["id"], employer["name"], employer.get("description"), employer.get("alternate_url"))
        )
        cursor.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_vacancy(conn: psycopg2.extensions.connection, vacancy: Dict[str, Any]) -> None:
    """Вставляет данные о вакансии в таблицу vacancies."""
    command = """
    INSERT INTO vacancies (vacancy_id, employer_id, name, description, salary, url)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (vacancy_id) DO NOTHING
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            command,
            (
                vacancy["id"],
                vacancy["employer"]["id"],
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
