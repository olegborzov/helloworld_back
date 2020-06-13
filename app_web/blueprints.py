from flask import Blueprint

from app_web.handlers import auth as api_auth
from app_web.handlers import ping as api_ping
from app_web.handlers import tasks as api_tasks

# Base
base_app = Blueprint("base", __name__, url_prefix='')
base_app.add_url_rule("/ping", 'ping', api_ping.ping, methods=['GET'])

# API Auth
api_auth_app = Blueprint("api_auth", __name__, url_prefix='/api/auth')
api_auth_app.add_url_rule("/me", 'me', api_auth.me, methods=['GET'])
api_auth_app.add_url_rule("/login", 'login', api_auth.login, methods=['POST'])
api_auth_app.add_url_rule("/register", 'register', api_auth.register, methods=['POST'])
api_auth_app.add_url_rule("/logout", 'logout', api_auth.logout, methods=['POST'])

# API Tasks
api_task_app = Blueprint("api_task", __name__, url_prefix='/api/task')
api_task_app.add_url_rule("/send_mail", 'send_mail', api_tasks.send_email, methods=['POST'])


##########################################################
# Here we declare all blueprints
##########################################################

all_blueprints = (base_app, api_auth_app, api_task_app)

##########################################################
