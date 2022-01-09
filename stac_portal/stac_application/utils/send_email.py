import threading
from django.core.mail import EmailMessage

from stac_portal.settings import EMAIL_HOST_USER


def send_email(subject, body, to):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=EMAIL_HOST_USER,
        to=to
    )
    try:
        email.send()
    except Exception as e:
        pass


def send_email_async(subject, body, to):
    email_thread = threading.Thread(target=send_email, args=(subject, body, to,))
    email_thread.start()
