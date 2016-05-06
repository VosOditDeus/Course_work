from django.conf.urls import patterns, url
from Course_work import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^login/$',
                           'django.contrib.auth.views.login', name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
                       url(r'^logout-then-login/$', 'django.contrib.auth.views.logout_then_login',
                           name='logout_then_login'),
                       url(r'^password-change/$', 'django.contrib.auth.views.password_change', name='password_change'),
                       url(r'^password-change/done/$', 'django.contrib.auth.views.password_change_done',
                           name='password_change_done'),
                       # restore password urls
                       url(r'^password-reset/$', 'django.contrib.auth.views.password_reset',
                           name='password_reset'),
                       url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done',
                           name='password_reset_done'),
                       url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
                           'django.contrib.auth.views.password_reset_confirm',
                           name='password_reset_confirm'),
                       url(r'^password-reset/complete/$', 'django.contrib.auth.views.password_reset_complete',
                           name='password_reset_complete'),
                       url(r'^register/', 'accounts.views.registration', name='register'),
                       )

if settings.DEBUG == "True":
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
