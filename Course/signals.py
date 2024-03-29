from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from Course.models import work, competition
from actions.models import Action

@receiver(pre_delete, sender=work)
def work_post_delete_handler(sender, **kwargs):
    work = kwargs['instance']
    storage, path = work.work.storage, work.work.path
    storage.delete(path)
    action = Action.objects.get(id=work.id)
    if action:
        Action.delete(action)

@receiver(pre_delete,sender=competition)
def competition_post_delete_handler(sender,**kwargs):
    competition = kwargs['instance']
    storage, path = competition.logo.storage, competition.logo.path
    storage.delete(path)
    action = Action.objects.get(id=competition.id)
    if action:
        Action.delete(action)
