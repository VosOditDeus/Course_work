from .models import Action
from Course.models import profile


def actions(request):
    if request.user in profile.objects.all():
        action_list = Action.objects.exclude(user=request.user)[:10]
    else:
        action_list = Action.objects.all().order_by('-pk')[:10]
    return {'actions': action_list}


def user(request):
    return {'user':request.user}