from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Action(models.Model):
    user = models.ForeignKey(User, related_name='actions', db_index=True)
    verb = models.CharField(_('verb'), max_length=255)
    created = models.DateTimeField(_('created'), auto_now_add=True, db_index=True)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj')
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    class Meta:
        ordering =('-created',)