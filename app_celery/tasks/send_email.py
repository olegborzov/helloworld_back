from celery import Task

from config import Config
from app_celery.utils import email


class SendMailTask(Task):
    name = 'send_mail_task'

    def run(self, mail: str, message: str):
        email.send_mail(
            subject='Привет, мир!',
            message=message,
            recipients=[mail],
            smtp_server=Config.SMTP_SERVER,
            smtp_port=Config.SMTP_PORT,
            sender_mail=Config.SMTP_LOGIN,
            sender_pass=Config.SMTP_PASS
        )
