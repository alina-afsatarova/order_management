# Order Management (Cистема управления заказами в кафе)
Order Management - веб-приложение на Django для управления заказами в кафе.

## Развертывание проекта локально
В терминале выполните команду по клонированию репозитория:
```
git clone https://github.com/alina-afsatarova/order_management.git
```
Перейдите в склонированный репозиторий:
```
cd order_management
```
Cоздайте и активируйте виртуальное окружение:
```
python3 -m venv env
```
```
source venv/bin/activate
```
Установите зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Создайте файл .env и заполните его в соответствии с файлом .env.example
```
touch .env
```
Выполните миграции
```
cd order_management
```
```
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver
```
## Наполнение БД
Чтобы наполнить БД тестовыми данными выполните команды из корневой директории:
```
cd order_management
```
```
python manage.py loaddata db.json
```
## Создание суперпользователя и админка
Создайте суперпользователя командой в терминале:
```
python manage.py createsuperuser
```
Админ-зона Django доступна по адресу: `http://127.0.0.1:8000/admin/`.
## Документация Swagger
Документация для API доступна по адресу: `http://127.0.0.1:8000/api/docs/`.
## Запуск тестов
Для запуска тестов выполните команды из корневой директории:
```
cd order_management
```
```
pytest
```
Доступны тесты для приложений `orders` и `api`
