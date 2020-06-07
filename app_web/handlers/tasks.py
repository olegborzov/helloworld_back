from flask import g

from app_celery.tasks import SendMailTask
from app_web.schemas.tasks import SendMailSchema
from app_web.utils.decorators import login_required
from app_web.utils.response_json import success
from app_web.utils.validate_request import validate_request_json


@login_required
@validate_request_json(SendMailSchema)
def send_email():
    email = g.validated_json['email']
    message = g.validated_json['message']
    SendMailTask().delay(mail=email, message=message)
    return success(True)
