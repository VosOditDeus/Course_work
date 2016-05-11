from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


def upload_location(instance, filename):
    return '%s/%s' %(instance.name, filename)
def upload_location2(instance, filename):
    return '%s/%s' %(instance.logo, filename)


# Create your models here.
class profile(models.Model):
    ''' Need to rewrite Base user class'''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    facility = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    is_student = models.BooleanField(default=False)
    # def get_absolute_url(self):
    #     return reverse('student:student_detail', args=[self.user.username])
    def __unicode__(self):
        return "%s" %(self.user)
    @property
    def full_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class work(models.Model):
    work = models.FileField(upload_to=upload_location, blank=True, null=True)
    name = models.CharField(max_length=250)
    publish = models.DateTimeField(default=timezone.now,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to=upload_location)
    tcontent = models.TextField()
    author = models.ForeignKey(profile)
    slug = models.SlugField(unique_for_date='created', max_length=250,null=True, blank=True)
    def get_absolute_url(self):
        return reverse('work:work_detail', args=[self.name]) #rework shit
    def __unicode__(self):
        return "%s" %(self.name)
    @receiver(pre_delete,sender=work)
    def work_post_delete_handler(sender, **kwargs):
        work = kwargs['instance']
        storage, path = work.work.storage, work.work.path
        storage.delete(path)


class city(models.Model):
    '''Fill with city names, at least.'''
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return '%s' % (self.name)


class competition(models.Model):
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    STATUS_CHOICES = (
        (RUNNING, 'RUNNING'),
        (COMPLETED, 'COMPLETED'),
                     )
    begin_date = models.DateField()
    final_date = models.DateField()
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=upload_location2)
    city = models.ForeignKey(city, blank=True, null=True)
    created_by = models.ForeignKey(User)
    description = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=9, default='RUNNING')
    students = models.ManyToManyField(profile, related_name='participant')
    def __unicode__(self):
        return '%s' %(self.name)
    def duration(self,begin_date,final_date):
        return final_date - begin_date
    def get_absolute_url(self):
        return reverse('competition:competition_detail', args=[self.name]) #rework shit


class work_for_competition(models.Model):
    FIRST = '1'
    SECOND = '2'
    THIRD = '3'
    OTHERS = 'Other'
    TBA = 'TBA'
    PLACE_CHOICES = (
        (FIRST, '1'),
        (SECOND, '2'),
        (THIRD, '3'),
        (OTHERS, 'Other'),
        (TBA, 'TBA')
                    )
    work_name = models.ForeignKey(work, null=True, blank=True)
    competition = models.ForeignKey(competition, null=True, blank=True)
    place = models.CharField(choices=PLACE_CHOICES, max_length=6, default='TBA')
    # students = models.ForeignKey(profile)

    class Meta:
        ordering = ['place']
    def __unicode__(self):
        return self.competition.name


class Comment(models.Model):
    competition = models.ForeignKey(competition, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __unicode__(self):
        return 'Comment by %s on %s' % (self.name, self.competition)