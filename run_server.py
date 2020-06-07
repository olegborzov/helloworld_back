# This Python file uses the following encoding: utf-8

import os
from core.registry import create_registry

env = os.getenv("FLASK_ENV", 'local')  # local, test, development or production
env_type = os.getenv("FLASK_ENV_TYPE", 'local')  # web or celery

reg = create_registry(env=env, env_type=env_type)
app = reg.app
db = reg.db
celery = reg.celery


if __name__ == '__main__':
    is_debug = "dev" in reg.config.ENV
    reg.app.run(host='0.0.0.0', port=5000, debug=is_debug)
