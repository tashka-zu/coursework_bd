from typing import Any, Dict, List

import requests


def get_employers(employer_ids: List[int]) -> List[Dict[str, Any]]:
    """Получает данные о работодателях по их идентификаторам"""
    employers = []
    for employer_id in employer_ids:
        url = f"https://api.hh.ru/employers/{employer_id}"
        response = requests.get(url)
        if response.status_code == 200:
            employers.append(response.json())
    return employers


def get_vacancies(employer_id: int) -> List[Dict[str, Any]]:
    """Получает данные о вакансиях для конкретного работодателя"""
    url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["items"]
    return []


def search_employers(keyword: str) -> List[int]:
    """Поиск работодателей по ключевому слову"""
    url = "https://api.hh.ru/employers"
    params = {"text": keyword}
    response = requests.get(url, params=params)
    employer_ids = []
    if response.status_code == 200:
        employers = response.json()["items"]
        for employer in employers:
            employer_ids.append(employer["id"])
            print(f"Company: {employer['name']}, ID: {employer['id']}")
    return employer_ids
