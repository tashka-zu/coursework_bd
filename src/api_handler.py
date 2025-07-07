from typing import Any, Dict, List

import psycopg2
import requests

from database_setup import insert_employer, insert_vacancy


def search_employers(keyword: str, count: int = 10) -> List[int]:
    """
    Поиск работодателей по ключевому слову и возвращение их идентификаторов.
    """
    url = "https://api.hh.ru/employers"
    params = {"text": keyword, "per_page": count}
    response = requests.get(url, params=params)
    employer_ids = []

    if response.status_code == 200:
        employers = response.json()["items"]
        for employer in employers:
            employer_ids.append(employer["id"])

    return employer_ids


def get_vacancies(per_page: int = 100) -> List[Dict[str, Any]]:
    """
    Получает данные о вакансиях без фильтрации по компании.
    """
    url = f"https://api.hh.ru/vacancies?per_page={per_page}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["items"]
    return []


def load_data_to_database(conn: psycopg2.extensions.connection) -> None:
    """
    Загружает данные о компаниях и вакансиях в базу данных.
    """
    keyword = "IT"
    print(f"Поиск компаний по ключевому слову: {keyword}")
    employer_ids = search_employers(keyword, count=10)
    print(f"Найдено компаний: {len(employer_ids)}")

    for employer_id in employer_ids:
        employer_data = get_employer_data(employer_id)
        if employer_data:
            print(f"Добавление данных о компании с ID: {employer_id}")
            insert_employer(conn, employer_data)
            vacancies = get_vacancies(employer_id)
            print(f"Найдено вакансий для компании {employer_id}: {len(vacancies)}")
            for vacancy in vacancies:
                print(f"Добавление вакансии: {vacancy['name']}")
                insert_vacancy(conn, vacancy)


def get_employer_data(employer_id: int) -> Dict[str, Any]:
    """
    Получает данные о работодателе по его идентификатору.
    """
    url = f"https://api.hh.ru/employers/{employer_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}
