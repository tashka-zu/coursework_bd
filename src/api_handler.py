import requests

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