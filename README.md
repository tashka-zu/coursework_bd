# HH.ru Vacancy Data Project

Мой проект направлен на получение данных о компаниях и вакансиях с сайта hh.ru, их хранение в базе данных PostgreSQL и предоставление интерфейса для взаимодействия с этими данными.

## Предварительные требования

Перед запуском проекта убедитесь, что у вас установлена и настроена база данных PostgreSQL. Вам нужно создать базу данных и пользователя с соответствующими правами доступа.

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/ваш_репозиторий.git

2. Перейдите в директорию проекта:

   ```bash
   cd ваш_проект

3. Установите необходимые зависимости:

   ```bash
   pip install -r requirements.txt

4. Создайте файл .env в корневой директории проекта и укажите параметры подключения к базе данных:
   
5. ```bash
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=your_db_port
   
## Использование

Пример использования функций для работы с API hh.ru

```python
from api_handler import get_employers, get_vacancies

# Получение данных о работодателях
employer_ids = [123, 456, 789]
employers = get_employers(employer_ids)
print(employers)

# Получение данных о вакансиях для конкретного работодателя
vacancies = get_vacancies(employer_ids[0])
print(vacancies)
```

Пример использования функций для работы с базой данных

```python
from database_setup import create_connection, create_tables, insert_employer, insert_vacancy

# Создание подключения к базе данных и таблиц
conn = create_connection()
create_tables(conn)

# Вставка данных о работодателе и вакансиях
employer_data = {'id': 123, 'name': 'Example Company', 'description': 'Example Description', 'alternate_url': 'http://example.com'}
insert_employer(conn, employer_data)

vacancy_data = {'id': 1, 'employer': {'id': 123}, 'name': 'Example Vacancy', 'description': 'Example Vacancy Description', 'salary': {'from': 100000}, 'alternate_url': 'http://example.com/vacancy'}
insert_vacancy(conn, vacancy_data)

# Закрытие соединения
conn.close()
```

Пример использования интерфейса пользователя

```python
from user_interface import main

# Запуск интерфейса пользователя
main()
```

Пример использования класса DBManager

```python
from db_manager import DBManager

# Создание экземпляра DBManager
db_manager = DBManager()

# Получение списка всех компаний и количества вакансий у каждой компании
companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
for company, count in companies_and_vacancies:
    print(f"Company: {company}, Vacancies: {count}")

# Получение списка всех вакансий
all_vacancies = db_manager.get_all_vacancies()
for vacancy in all_vacancies:
    print(vacancy)

# Закрытие соединения
db_manager.close()
```

## Тестирование

На данный момент проект не включает автоматические тесты. Однако вы можете вручную протестировать функциональность, запуская различные части кода и проверяя результаты. В будущем планируется добавить модульные тесты для проверки функциональности API, базы данных и интерфейса пользователя.
