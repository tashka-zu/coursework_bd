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

# Пример использования
if __name__ == "__main__":
    # Пример списка идентификаторов работодателей
    example_employer_ids = [123, 456, 789]  # Замените на реальные идентификаторы
    employers = get_employers(example_employer_ids)
    print(employers)

    vacancies = get_vacancies(example_employer_ids[0])
    print(vacancies)
