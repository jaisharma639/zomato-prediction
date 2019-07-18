from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email

def send_email(subject, msg, to_mail):
    if not isinstance(to_mail, list):
        to_mail = list(to_mail)
    [validate_email(mail) for mail in to_mail]
    return send_mail(subject, msg, settings.EMAIL_HOST_USER,
                     to_mail, fail_silently=False)
