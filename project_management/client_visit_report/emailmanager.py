from django.core.mail import EmailMultiAlternatives
from email.utils import formataddr



def send(recipient, sender, subject, text_body, html_body=None):
    recipients = [formataddr((recipient.username, recipient.email))]
    msg = EmailMultiAlternatives(subject, text_body, to=recipients,
                                 reply_to=[sender.email])
    if html_body:
        msg.attach_alternative(html_body, "text/html")
    if msg.send():
        return True
    else:
        return False
