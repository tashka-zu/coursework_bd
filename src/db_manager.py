import os
from typing import Any, List, Optional, Tuple

import psycopg2
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()


class DBManager:
    def __init__(self) -> None:
        """Инициализация соединения с базой данных."""
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )

    def get_companies_and_vacancies_count(self) -> List[Tuple[Any, ...]]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT e.name, COUNT(v.vacancy_id) as vacancy_count
                FROM employers e
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                GROUP BY e.name
            """
            )
            return cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple[Any, ...]]:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии,
        зарплаты и ссылки на вакансию
        Возвращает список кортежей, где каждый кортеж содержит информацию о вакансии
        """
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT e.name, v.name as vacancy_name, v.salary, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
            """
            )
            return cursor.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """
        Получает среднюю зарплату по вакансиям.
        Возвращает среднюю зарплату или None, если данные отсутствуют
        """
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT AVG(CAST(salary AS FLOAT)) as avg_salary
                FROM vacancies
                WHERE salary IS NOT NULL
            """
            )
            result = cursor.fetchone()
            return result[0] if result else None

    def get_vacancies_with_higher_salary(self) -> List[Tuple[Any, ...]]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        Возвращает список кортежей с информацией о вакансиях
        """
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT e.name, v.name as vacancy_name, v.salary, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE CAST(v.salary AS FLOAT) > %s
            """,
                (avg_salary,),
            )
            return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[Any, ...]]:
        """
        Получает список всех вакансий, в названии которых содержатся переданные слова.
        Возвращает список кортежей с информацией о вакансиях
        """
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT e.name, v.name as vacancy_name, v.salary, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE v.name ILIKE %s
            """,
                (f"%{keyword}%",),
            )
            return cursor.fetchall()

    def close(self) -> None:
        """Закрывает соединение с базой данных"""
        self.conn.close()
