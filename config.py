# This Python file uses the following encoding: utf-8

import os

from envparse import Env

basedir = os.path.abspath(os.path.dirname(__file__))
env = Env()
env_file = os.environ.get('ENV', 'dev') + ".env"
env_file_path = os.path.join(basedir, 'conf', '.env_files', env_file)
env.read_envfile(env_file_path)


def get_path(*parts):
    return os.path.join(basedir, *parts)


class Config:
    NAME = env.str("NAME", default="hello_world")

    ENV = env.str("ENV", default="dev")
    DEBUG = env.bool("DEBUG", default=True)
    TESTING = env.bool("TESTING", default=False)
    SECRET_KEY = env.str("FLASK_SECRET_KEY", default="secret_key")

    # DB
    POSTGRES_USER = env.str("POSTGRES_USER", default="")
    POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD", default="")
    POSTGRES_DB_HOST = env.str("POSTGRES_DB_HOST", default="localhost")
    POSTGRES_DB_PORT = env.int("POSTGRES_DB_PORT", default=5433)
    POSTGRES_DB = env.str("POSTGRES_DB", default="helloworld_db")

    SQLALCHEMY_DATABASE_URI = "{schema}://{login}:{password}@{host}:{port}/{db_name}".format(
        schema="postgresql",
        login=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_DB_HOST,
        port=POSTGRES_DB_PORT,
        db_name=POSTGRES_DB
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': env.int("SQLALCHEMY_POOL_SIZE", default=5),
        'max_overflow': env.int("SQLALCHEMY_MAX_OVERFLOW", default=2),
        'pool_timeout': env.int("SQLALCHEMY_POOL_TIMEOUT", default=60),
    }
    SQLALCHEMY_ECHO = env.bool("SQLALCHEMY_ECHO", default=True)
    SQLALCHEMY_TRACK_MODIFICATIONS = env.bool("SQLALCHEMY_TRACK_MODIFICATIONS", default=False)

    RABBITMQ_URI = "{schema}://{login}:{password}@{host}:{port}/{vhost}".format(
        schema="pyamqp",
        login=env.str("RABBITMQ_DEFAULT_USER", default=""),
        password=env.str("RABBITMQ_DEFAULT_PASS", default=""),
        host=env.str("RABBITMQ_HOST", default="localhost"),
        port=env.int("RABBITMQ_PORT", default=5672),
        vhost=env.str("RABBITMQ_DEFAULT_VHOST", default='vhost'),
    )
    REDIS_URI = "{schema}://{login}:{password}@{host}:{port}/".format(
        schema="redis",
        login=env.str("REDIS_LOGIN", default=""),
        password=env.str("REDIS_PASSWORD", default=""),
        host=env.str("REDIS_HOST", default="localhost"),
        port=env.int("REDIS_PORT", default=6379),
    )

    CELERY_CONFIG = dict(
        broker_url=RABBITMQ_URI,
        result_backend=REDIS_URI,
        accept_content=["pickle", "json"],
        task_serializer='pickle',
        result_serializer='json',
        task_ignore_result=False,

        imports=('app_celery.periodic', ),
        beat_schedule=(),
        timezone="Europe/Moscow",

        # Raise exc if task takes too long
        task_soft_time_limit=env.int("CELERY_SOFT_TIME_LIMIT", default=5*60),
        # Kill worker if task too long
        task_time_limit=env.int("CELERY_TASK_TIME_LIMIT", default=10*60),
    )

    # EMAIL Reports Credentials
    SMTP_LOGIN = env.str("SMTP_LOGIN", default="rambler.seo.reports@gmail.com")
    SMTP_PASS = env.str("SMTP_PASS", default="a$3sdj1kh")
    SMTP_SERVER = env.str("SMTP_SERVER", default="smtp.gmail.com")
    SMTP_PORT = env.int("SMTP_PORT", default=587)
