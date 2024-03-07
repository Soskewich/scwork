# Аналитическая система ОмГТУ
Web-система осуществляющая сбор и хранение данных о сотрудниках, публикациях, источниках. Проект размещен на https://science.omgtu.ru/

Сбор данных произходит из:
- OpenAlex
- Scopus
- Elibrary
- RSCI
- "Белый список"  РЦНИ
- WoS JCR

## Запуск и установка
Перед запуском в корневой папке и папке backend необходимо создать .env файлы. Примеры находятся в соответствующих папках (env_example). В папке frontend/src нужно создать файл settings.js (пример в файле settings_example_js)
Также необходимо добавить ssl сертификаты в папку nginx/certs (fullchain.pem, privkey.pem)

Для запуска приложения необходим docker-compose. 
Выполните следующие команды
```sh
docker-compose build
docker-compose up
```

## Используемые технологии

 Контейнеризация:
- Docker
- docker-compose

База данных
- Postgres

Backend:
- FastAPI
- aiohttp
- SqlAlchemy
- asyncpg
- pandas
- Pytest

Frontend:
- Redux-toolkit
- react-router-dom
- CSS Modules
- axios
- react-cookie


Обратный прокси сервер: 
- Nginx
