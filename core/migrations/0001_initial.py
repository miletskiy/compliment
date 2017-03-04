# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250, null=True, verbose_name='Title', blank=True)),
                ('description', models.TextField(default='', verbose_name='Description', blank=True)),
                ('preview', models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photos',
            },
        ),
        migrations.CreateModel(
            name='UsersPhoto',
            fields=[
                ('photo_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Photo')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'UsersPhoto',
                'verbose_name_plural': 'UsersPhotos',
            },
            bases=('core.photo',),
        ),
    ]
