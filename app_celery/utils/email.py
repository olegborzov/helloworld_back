#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from typing import Dict, List, Optional

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from premailer import transform


def send_mail(subject: str, message: str, recipients: List[str],
              sender_mail: str, sender_pass: str,
              smtp_server: str, smtp_port: int = 587,
              images: Optional[Dict[str, bytes]] = None):
    smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
    smtp_obj.starttls()
    smtp_obj.login(sender_mail, sender_pass)

    # Текст сообщения:
    # Как формировать - https://docs.python.org/2/library/email-examples.html
    message = transform(message)

    if images:
        msg = MIMEMultipart("related")
        msg_html = MIMEText(message, 'html')
        msg.attach(msg_html)

        for img_name, img in images.items():
            msg_img = MIMEImage(img, 'png')
            msg_img.add_header('Content-ID', "<%s>" % img_name)
            msg_img.add_header(
                'Content-Disposition', 'inline', filename=f"img_name.png"
            )
            msg_img.add_header(
                'Content-Disposition', 'attachment', filename=f"img_name.png"
            )
            msg.attach(msg_img)
    else:
        msg = MIMEText(message, "html")

    msg["Subject"] = subject
    msg["From"] = sender_mail
    msg["To"] = ', '.join(recipients)

    smtp_obj.sendmail(sender_mail, recipients, msg.as_string())
    smtp_obj.quit()
