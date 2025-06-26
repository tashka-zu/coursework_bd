import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

class DBManager:
    def __init__(self):
        """Инициализация соединения с базой данных."""
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, COUNT(v.vacancy_id) as vacancy_count
                FROM employers e
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                GROUP BY e.name
            """)
            return cursor.fetchall()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии,
        зарплаты и ссылки на вакансию.
        """
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, v.name as vacancy_name, v.salary, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
            """)
            return cursor.fetchall()

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT AVG(CAST(salary AS FLOAT)) as avg_salary
                FROM vacancies
                WHERE salary IS NOT NULL
            """)
            result = cursor.fetchone()
            return result[0] if result else None

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, v.name as vacancy_name, v.salary, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE CAST(v.salary AS FLOAT) > %s
            """, (avg_salary,))
            return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные слова.
        """
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, v.name as vacancy_name, v.salary, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE v.name ILIKE %s
            """, (f'%{keyword}%',))
            return cursor.fetchall()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.conn.close()

# Пример использования
if __name__ == "__main__":
    db_manager = DBManager()

    print("Companies and their vacancies count:")
    companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
    for company, count in companies_and_vacancies:
        print(f"{company}: {count}")

    print("\nAll vacancies:")
    all_vacancies = db_manager.get_all_vacancies()
    for vacancy in all_vacancies:
        print(vacancy)

    avg_salary = db_manager.get_avg_salary()
    print(f"\nAverage salary: {avg_salary}")

    print("\nVacancies with higher salary than average:")
    higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    for vacancy in higher_salary_vacancies:
        print(vacancy)

    keyword = "python"
    print(f"\nVacancies with keyword '{keyword}':")
    keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
    for vacancy in keyword_vacancies:
        print(vacancy)

    db_manager.close()
