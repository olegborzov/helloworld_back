# This Python file uses the following encoding: utf-8

"""
Registry with global objects (apps, config, db, managers)
"""
import os

from celery import Celery
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from core import manager
from core.classes import SingletonMeta

celery = Celery()
db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()
cors = CORS(resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

envs_dict = {
    "local": "local",
    "development": "dev",
    "dev": "dev",
    "production": "prod",
    "prod": "prod",
    "test": "test",
    "testing": "test"
}


class Registry(metaclass=SingletonMeta):
    config = None
    app: Flask
    celery: Celery
    db: SQLAlchemy
    migrate: Migrate

    manager: manager.DefaultManager

    def __init__(self, env: str):
        self._set_config(env)

        # Create apps
        self.set_flask_app()
        self.set_db()
        self._set_migrate_app()
        self._set_celery_app()

        # Create and init managers
        self._set_manager()
        self._init_manager()

    def set_flask_app(self):
        import config as conf

        self.app = Flask(
            self.config.NAME,
            template_folder=conf.get_path("app_web", "templates"),
            static_folder=conf.get_path("app_web", "static")
        )
        self.app.config.from_object(self.config)
        self.app.app_context().push()

    def _set_celery_app(self):
        self.celery = celery
        self.celery.main = self.app.import_name
        self.celery.conf.update(self.app.config['CELERY_CONFIG'])

        class ContextTask(self.celery.Task):
            def __call__(self, *args, **kwargs):
                if hasattr(self.app, 'app_context'):
                    with self.app.app_context():
                        return self.run(*args, **kwargs)
                else:
                    return self.run(*args, **kwargs)

        self.celery.Task = ContextTask
        self.register_celery_tasks()

    def register_celery_tasks(self):
        from app_celery.tasks import all_task_classes
        for task_class in all_task_classes:
            self.celery.register_task(task_class())

    def set_db(self):
        self.db = db
        self.db.init_app(self.app)

    def _set_migrate_app(self):
        self.migrate = Migrate(self.app, self.db)

    def _set_manager(self):
        self.manager = self.__annotations__['manager']()
        self.manager.marshmallow = ma

    def _init_manager(self):
        for name, mngr in self.manager.as_dict().items():
            mngr.init_app(self.app)

    def _set_config(self, env: str):
        os.environ['ENV'] = env

        import config as conf
        self.config = conf.Config()


class WebRegistry(Registry):
    manager: manager.WebManager

    def __init__(self, env: str):
        super().__init__(env)

    def _set_manager(self):
        super()._set_manager()
        self.manager.login = login_manager
        self.manager.cors = cors

    def _init_manager(self):
        super()._init_manager()
        self._register_blueprints()

    def _register_blueprints(self):
        from app_web.blueprints import all_blueprints

        for bp in all_blueprints:
            self.app.register_blueprint(bp)


class CeleryRegistry(Registry):
    pass


def create_registry(env: str, env_type: str) -> Registry:
    env = envs_dict.get(env, 'dev')

    if "web" in env_type:
        return WebRegistry(env)
    elif "celery" in env_type:
        return CeleryRegistry(env)
    else:
        return WebRegistry(env)

