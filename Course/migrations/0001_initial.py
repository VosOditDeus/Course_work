# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 12:13
from __future__ import unicode_literals

import Course.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='city',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_date', models.DateField()),
                ('final_date', models.DateField()),
                ('name', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to=Course.models.upload_location2)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('RUNNING', 'RUNNING'), ('COMPLITED', 'COMPLITED')], default='RUNNING', max_length=9)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Course.city')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('second_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('age', models.IntegerField()),
                ('facility', models.CharField(max_length=100)),
                ('bio', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work', models.FileField(blank=True, null=True, upload_to=Course.models.upload_location)),
                ('name', models.CharField(max_length=250)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(upload_to=Course.models.upload_location)),
                ('tcontent', models.TextField()),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique_for_date='created')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.student')),
            ],
        ),
        migrations.CreateModel(
            name='work_for_competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('Other', 'Other'), ('TBA', 'TBA')], default='TBA', max_length=6)),
                ('students', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.student')),
            ],
        ),
        migrations.AddField(
            model_name='competition',
            name='studens',
            field=models.ManyToManyField(related_name='part', to='Course.student'),
        ),
        migrations.AddField(
            model_name='comment',
            name='competition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Course.competition'),
        ),
    ]