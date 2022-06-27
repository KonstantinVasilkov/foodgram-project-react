# Сайт "Продуктовый помощник FoodGram"

***Это сайт, на котором пользователи будут публиковать рецепты, добавлять 
чужие 
рецепты в избранное и подписываться на публикации других авторов. Сервис 
«Список покупок» позволит пользователям создавать список продуктов, которые
нужно купить для приготовления выбранных блюд.***
___________________
## Стек технологий и статус *workflow*:

[![Python](https://camo.githubusercontent.com/f13f8c8fd603bd94f3c006d5650ea82b0213e94c54ac4b93e1d56f765a068882/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4d616465253230776974682d507974686f6e2d677265656e3f6c6f676f3d707974686f6e266c6f676f436f6c6f723d776869746526636f6c6f72)](https://www.python.org/) 
[![Docker](https://camo.githubusercontent.com/68b1b15acde4efc8a882ad9dc399d73a7d72d6ffb69fd47f95c60772976d1218/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76313f6d6573736167653d646f636b6572266c6f676f3d646f636b6572266c6162656c436f6c6f723d35633563356326636f6c6f723d303032633636266c6f676f436f6c6f723d7768697465266c6162656c3d253230267374796c653d706c6173746963)](https://www.docker.com/)
[![Django](https://camo.githubusercontent.com/36cd67e6d0292012b0c84f7ca1c60697fe15d9c2a5a8171d2229a877f321298d/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76313f6d6573736167653d646a616e676f266c6f676f3d646a616e676f266c6162656c436f6c6f723d35633563356326636f6c6f723d306334623333266c6f676f436f6c6f723d7768697465266c6162656c3d253230267374796c653d706c6173746963)](https://www.djangoproject.com/)
[![Nginx](https://camo.githubusercontent.com/ea3d94458fad94b44b35ed0d03b6cf7bc2054d334d6f669f29807fa7a52ab90d/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76313f6d6573736167653d6e67696e78266c6f676f3d6e67696e78266c6162656c436f6c6f723d35633563356326636f6c6f723d303039393030266c6f676f436f6c6f723d7768697465266c6162656c3d253230267374796c653d706c6173746963)](https://nginx.org/)
[![Postgres](https://camo.githubusercontent.com/ad8e4b6c04b8f9caec8d7c47e9d79110724148c57282007ca247424871f3626f/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76313f6d6573736167653d706f737467726573716c266c6f676f3d706f737467726573716c266c6162656c436f6c6f723d35633563356326636f6c6f723d313138326333266c6f676f436f6c6f723d7768697465266c6162656c3d253230267374796c653d706c6173746963)](https://www.postgresql.org/)
![Actions Status](https://github.com/KonstantinVasilkov/foodgram-project-react/actions/workflows/main.yml/badge.svg)
_____________________

## Описание работы сайта

После регистрации на сайте пользователь может добавлять собственные рецепты,
просматривать рецепты, добавленные другими пользователями. При помощи тегов,
пользователь легко может подобрать себе меню на конкретный приём пищи, а 
функция "добавить в список покупок" позволяет выгрузить полный список 
ингредиентов, необходимых для приготовления понравившихся блюд и пойти с 
ним в магазин. 

## Разворачивание проекта локально:
1. Скачайте репозиторий:
``` bash
$ git clone git@github.com:KonstantinVasilkov/foodgram-project-react.git
```
2. Перейти в папку проекта:
``` bash
$ cd ./foodgram-project-react
```
3. Создать виртуальное окружение:
``` bash
$ python3 -m venv venv
$ . venv/bin/activate
```
4. Установить зависимости:
``` bash
$ pip install -r requirments.txt
```
5. Подготовить файл с переменными окружения:

```
Пример файла .env:
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='my_super_secret_key'
ALLOWED_HOSTS="localhost|84.201.139.50"
DEBUG=False
```
6. Установить docker и docker-compose
7. Перейти в папку `./infra` и запустить контейнеры
``` bash
$ sudo docker-compose up
```





### адрес сервера: `http://84.201.139.50/`
### login: `admin@mail.com`
### password: `admin`
