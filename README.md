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

Установить переменные окружения
```
$ export FLASK_APP=run_server.py    #
$ export FLASK_ENV=development      # Environment
$ export FLASK_DEBUG=1              # Don't need usually
```

##Docker
Запуск контейнеров
```
$ docker-compose -f docker-compose.db.yml up -d
$ docker-compose -f docker-compose.workers.yml up -d
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
$ docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```


##Flask
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
