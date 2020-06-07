from app_celery.tasks.send_email import SendMailTask

all_task_classes = [SendMailTask]
