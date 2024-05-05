# Wishlist App
## Цель проекта
Простое приложение для тренеровки навыков коллаборации и фронтенд разработки
## Идея, референсы:
[Проект страниц на фигме](https://www.figma.com/file/SDVfww85t5gPb2FvjZHCih/Untitled?type=design&node-id=30%3A4&mode=design&t=FFtuxxU0AVOWdCcn-1)
## Требования
Docker
docker compose
Python 3.11+
Django 5+
## Инструкции для Юры
* Склонировать себе
```bash
git clone
```
* создать виртуальное окружение (по желанию)
```bash
virtualenv wish-env
.\wish-env\Scripts\activate
```
* запустить бд
```bash
docker compose up -d
```
* применить миграции
```bash
python manage.py makemigrations
python manage.py migrate
```
* собрать статику
```bash
python manage.py collectstatic
```
* установить зависимости
```bash
pip install -r requirements.txt
```
* дописать фронтенд

### TODO:
* написать бек (совместно)
* написать фронт (Samuray)
* по готовности приложения приложения поменять ридми на что то вменяемое, авось кому пригодится