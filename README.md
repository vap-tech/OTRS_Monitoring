# OTRS_Monitoring

Скрипт мониторит тикеты в заданной очереди OTRS по ключевому слову.
Ключевое слово проверяется на вхождение в тему тикета.
По итогу проверки отсылаются уведомления в telegram. 

##### Запуск локально:
+ Переименовать .env.sample в .env
+ Внести необходимые параметры в .env
+ poetry shell
+ python3 main.py

##### Запуск Docker:
+ Переименовать .env-non-dev.sample в .env-non-dev
+ В файле .env-non-dev внести необходимые изменения
+ docker compose build
+ docker compose up
