from __future__ import unicode_literals

from django.apps import AppConfig


class CourseConfig(AppConfig):
    name = 'Course'
    verbose_name = 'Course Work'
    def ready(self):
        import Course.signals