from celery import task
from django.core.mail import send_mail
from .models import work
from django.contrib.auth.models import User

@task
def work_uploaded(work_id):
    """
    Task to send email when new
    competition created(form now console only)
    :param comp_id:
    :return: mail_sent
    """
    Work = work.objects.get(id=work_id)
    subject = 'Work %s was successful uploaded ' %(Work.name)
    massage = 'Students! There is new work %s' % (Work.name)
    mail_sent = send_mail(subject, massage, 'vosoditdeus@gmail.com',[work.objects.get(id=work_id).author.user.email],fail_silently=False )
    return mail_sent

