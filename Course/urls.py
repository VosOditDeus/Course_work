from django.conf.urls import patterns, url
from Course_work import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^student_detail/(?P<user>[-\w]+)/$', 'Course.views.student_detail', name='student_detail'),
                       url(r'^student_list/', 'Course.views.student_list', name='std_l'),
                       url(r'^edit/$', 'Course.views.edit', name='edit'),
                       url(r'^$', 'Course.views.index', name='main'),
                       url(r'^competition_detail/(?P<comp_id>\d+)/$', 'Course.views.competition_detail', name='detail'),
                       url(r'^work_detail/(?P<slug>[-\w]+)/$', 'Course.views.work_detail', name='work_d'),
                       url(r'^competition_list/$', 'Course.views.competition_list', name='comp_l'),
                       # url(r'^login/$', 'Course.views.user_login', name='login'),
                       url(r'^add_work/$', 'Course.views.upload_work', name='work_add'),
                       url(r'^sing_up/(?P<comp_id>\d+)/$', 'Course.views.sing_up', name='sing_up')
                       )
if settings.DEBUG == "True":
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# TODO: Change it on deploy, read django docs
