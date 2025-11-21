## Запуск приложения (локально):
1. Склонировать репозиторий:
git clone https://github.com/pavel-ladygin/django-askme
2. Активировать виртуальное окружение:
source venv/bin/activate  
3. Установить зависимоти:
pip install -r requirements.txt
4. Запуск локального сервера на порте 8000:
python manage.py runserver 

## Запуск приложения (docker):
1. Склонировать репозиторий:
git clone https://github.com/pavel-ladygin/django-askme
2. Запустить докер-контейнер:
docker-compose up --build -d
3. Применить миграции и запустить генерацию данных:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py filldb [ratio]
4. После окончания генерации открыть прилложение:
http://localhost:8000/