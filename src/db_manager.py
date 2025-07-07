import os
from typing import Any

import psycopg2
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )

    def get_companies_and_vacancies_count(self) -> Any:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT e.name, COUNT(v.vacancy_id)
                FROM employers e
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                GROUP BY e.name
            """
            )
            return cursor.fetchall()

    def get_all_vacancies(self) -> Any:
        """Получает список всех вакансий."""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT name, salary, url FROM vacancies")
            return cursor.fetchall()

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT AVG(CAST(REGEXP_REPLACE(salary, '[^0-9]', '', 'g') AS INTEGER))
                FROM vacancies
                WHERE salary IS NOT NULL
            """
            )
            result = cursor.fetchone()
            return result[0] if result else 0

    def get_vacancies_with_higher_salary(self) -> Any:
        """Получает список вакансий с зарплатой выше средней."""
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT name, salary, url
                FROM vacancies
                WHERE CAST(REGEXP_REPLACE(salary, '[^0-9]', '', 'g') AS INTEGER) > %s
            """,
                (avg_salary,),
            )
            return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> Any:
        """Получает список вакансий по ключевому слову."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT name, salary, url
                FROM vacancies
                WHERE name ILIKE %s
            """,
                (f"%{keyword}%",),
            )
            return cursor.fetchall()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.conn.close()
