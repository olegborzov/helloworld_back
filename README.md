# HelloWorld app
Простое приложение на Flask с возможностью регистрации, авторизации и отправки Email через Celery

### Автор
Борзов Олег<br>
http://olegborzov.ru/<br>

##Команды для запуска и настройки приложения 
Создать виртуальное окружение для Python:
```
$ virtualenv venv                   # Создать виртуальное окружение
$ source venv/bin/activate          # Войти в виртуальное окружение
```

##Docker
Запуск контейнеров
```
$ docker-compose -f docker-compose.local.db.yml up -d           # Запуск локального контейнера с БД
$ docker-compose -f docker-compose.local.workers.yml up -d      # Запуск локального окружения с воркерами
$ docker-compose -f docker-compose.dev.yml up -d                # Запуск dev окружения на сервере
$ docker-compose -f docker-compose.prod.yml up -d               # Запуск prod окружения на сервере
```

##Flask
Установить переменные окружения
```
$ export FLASK_APP=run_server.py    # Установка файла для запуска сервера
$ export FLASK_ENV=dev              # Установка окружения (local/test/dev/prod)
$ export FLASK_DEBUG=1              # Debug-режим
```

Запуск Flask приложения
```
$ flask run
```

Команды для миграций БД:
```
$ flask db init                     # Создание папки с миграциями
$ flask db migrate                  # При изменении моделей
$ flask db upgrade                  # Применение миграций к БД
```
