# HelloWorld backend
Простое приложение на Flask с возможностью регистрации, авторизации и отправки Email через Celery

### Автор
Борзов Олег<br>
http://olegborzov.ru/<br>

## Структура проекта
**Папки**
- **.ci-cd** - sh-скрипты для деплоя проекта на сервер
    - deploy.sh - деплой, запускается на сервере после билда и прогона тестов в Github Actions
    - rollback.sh - для отката деплоя на предыдущую версию
    - curl_tg.sh - для отправки уведомлений о процессе деплоя в Telegram
- **app_celery** - таски, выполняемые Celery
    - **periodic** (пусто) - периодические задания, выполняемые по крону или с указанным интервалом
    - **tasks** - обычные Celery таски
    - **utils** - вспомогательные функции и декораторы
- **app_web** - бек-часть
    - **handlers** - "ручки"
    - **schemas** - схемы валидации для ручек
    - **utils** - вспомогательные функции и декораторы
- **conf** - конфигурационные файлы
    - **.env_files** - файлы с переменными окружения для конфигурации
    - **docker** - docker-файлы 
- **core** - общие вспомогательные классы, функции и декораторы для проекта
    - **classes.py** - базовые классы (абстрактные и мета)
    - **decorators.py** - полезные декораторы
    - **manager.py** - менеджеры для Flask
    - **registry.py** - фабрика для создания и инициализации Flask приложения 
- **migrations** - файлы миграций AlembicЛ
- **models** - модели SQLAlchemy

**Файлы**<br>
- config.py - файл конфигурации для проекта (заполняется из переменных окружения)
- run_server.py - файл для запуска сервера


## Команды для запуска и настройки приложения 
Создать виртуальное окружение для Python:
```
$ virtualenv venv                   # Создать виртуальное окружение
$ source venv/bin/activate          # Войти в виртуальное окружение
```

Команды CI/CD
```
$ sh .ci-cd/deploy.sh ENV TG_BOT_TOKEN TG_CHAT_ID       # Запуск деплоя с новой версией
$ sh .ci-cd/rollback.sh ENV TG_BOT_TOKEN TG_CHAT_ID     # Откат деплоя на предыдущую версию
```

## Docker
Запуск контейнеров
```
$ docker-compose -f docker-compose.local.db.yml up -d           # Запуск локального контейнера с БД
$ docker-compose -f docker-compose.local.workers.yml up -d      # Запуск локального окружения с воркерами
$ docker-compose -f docker-compose.test.yml run test_web        # Запуск тестов
```

## Flask
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
