from typing import List, Optional, Tuple

import psycopg2
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="hh_data", user="postgres", password="tasha1502", host="localhost", port="5432"
        )

    def get_all_vacancies(self) -> List[Tuple[str, Optional[str], str]]:
        """Получает список всех вакансий."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT name, salary, url
                FROM vacancies
            """
            )
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

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, Optional[str], str]]:
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

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, Optional[str], str]]:
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
