import requests

def get_employers(employer_ids):
    """
    Получает данные о работодателях по их идентификаторам.

    :param employer_ids: Список идентификаторов работодателей.
    :return: Список данных о работодателях.
    """
    employers = []
    for employer_id in employer_ids:
        url = f"https://api.hh.ru/employers/{employer_id}"
        response = requests.get(url)
        if response.status_code == 200:
            employers.append(response.json())
    return employers

def get_vacancies(employer_id):
    """
    Получает данные о вакансиях для конкретного работодателя.

    :param employer_id: Идентификатор работодателя.
    :return: Список данных о вакансиях.
    """
    url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['items']
    return []

def search_employers(keyword):
    """
    Поиск работодателей по ключевому слову
    """
    url = f"https://api.hh.ru/employers"
    params = {'text': keyword}
    response = requests.get(url, params=params)
    employer_ids = []

    if response.status_code == 200:
        employers = response.json()['items']
        for employer in employers:
            employer_ids.append(employer['id'])
            print(f"Company: {employer['name']}, ID: {employer['id']}")

    return employer_ids

# Пример использования
if __name__ == "__main__":
    keyword = "Yandex"
    employer_ids = search_employers(keyword)
    print(employer_ids)