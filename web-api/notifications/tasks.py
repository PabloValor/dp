from __future__ import absolute_import
from celery import shared_task

def send_email():
    from django.core.mail import EmailMultiAlternatives

    msg = EmailMultiAlternatives(
        subject="Djrill Message",
        body="This is the text email body",
        from_email="Djrill Sender <djrill@example.com>",
        to=["nmbases@gmail.com"],
        headers={'Reply-To': "Service <support@example.com>"} # optional extra headers
    )
    msg.attach_alternative("<p>This is the HTML email body</p>", "text/html")

    # Optional Mandrill-specific extensions:
    msg.tags = ["one tag", "two tag", "red tag", "blue tag"]
    msg.metadata = {'user_id': "8675309"}

    # Send it:
    msg.send()

@shared_task
def send_notification_email(notification):
    send_email()

