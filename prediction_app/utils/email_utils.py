from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
import threading



def send_email(subject, msg, to_mail):
    if not isinstance(to_mail, list):
        to_mail = list(to_mail)
    [validate_email(mail) for mail in to_mail]
    args = (subject, msg, settings.EMAIL_HOST_USER, to_mail)
    thr = threading.Thread(target=send_mail, args=args, kwargs={'fail_silently':False})
    return thr.start()
