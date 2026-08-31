Проект позволяет добавлять интересующие темы, подтемы к ним и тестирование для закрепления знаний.

**Запуск проекта**

Создать виртуальное окружение и активировать:

    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate

Установить зависимости:

    pip install -r requirements.txt

Создать и применить миграции:

    python manage.py makemigrations
    python manage.py migrate

Создать суперпользователя:

    python manage.py createsuperuser

Запустить:

    python manage.py runserver


**Наполнение сайта**

Зайти в админку с помощью суперпользователя:
http://127.0.0.1:8000/admin/ 

Поле статьи "Text" поддерживает разметку **markdown**