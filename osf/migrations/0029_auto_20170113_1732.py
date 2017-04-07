# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-13 23:32
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import osf.utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('osf', '0028_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstractnode',
            name='discourse_post_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='abstractnode',
            name='discourse_project_contributors',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, default=b''), blank=True, default=None, null=True, size=None),
        ),
        migrations.AddField(
            model_name='abstractnode',
            name='discourse_project_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='abstractnode',
            name='discourse_project_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='abstractnode',
            name='discourse_project_public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='abstractnode',
            name='discourse_topic_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='abstractnode',
            name='discourse_topic_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='abstractnode',
            name='discourse_topic_parent_guids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, default=b''), blank=True, default=None, null=True, size=None),
        ),
        migrations.AddField(
            model_name='abstractnode',
            name='discourse_topic_title',
            field=models.TextField(blank=True, default=b''),
        ),
        migrations.AddField(
            model_name='abstractnode',
            name='discourse_view_only_keys',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, default=b''), blank=True, default=None, null=True, size=None),
        ),
        migrations.AddField(
            model_name='osfuser',
            name='discourse_apikey',
            field=models.TextField(blank=True, default=b''),
        ),
        migrations.AddField(
            model_name='osfuser',
            name='discourse_apikey_date_created',
            field=osf.utils.fields.NonNaiveDateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='osfuser',
            name='discourse_user_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='osfuser',
            name='discourse_user_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='osfuser',
            name='discourse_username',
            field=models.TextField(blank=True, default=b''),
        ),
        migrations.AddField(
            model_name='storedfilenode',
            name='discourse_post_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='storedfilenode',
            name='discourse_topic_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='storedfilenode',
            name='discourse_topic_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='storedfilenode',
            name='discourse_topic_parent_guids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, default=b''), blank=True, default=None, null=True, size=None),
        ),
        migrations.AddField(
            model_name='storedfilenode',
            name='discourse_topic_title',
            field=models.TextField(blank=True, default=b''),
        ),
        migrations.AddField(
            model_name='trashedfilenode',
            name='discourse_post_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='trashedfilenode',
            name='discourse_topic_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trashedfilenode',
            name='discourse_topic_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='trashedfilenode',
            name='discourse_topic_parent_guids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, default=b''), blank=True, default=None, null=True, size=None),
        ),
        migrations.AddField(
            model_name='trashedfilenode',
            name='discourse_topic_title',
            field=models.TextField(blank=True, default=b''),
        ),
    ]
