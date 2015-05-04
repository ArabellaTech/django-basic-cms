# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import basic_cms.utils
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=5, verbose_name='language')),
                ('body', models.TextField(verbose_name='body')),
                ('type', models.CharField(max_length=100, verbose_name='type', db_index=True)),
                ('creation_date', models.DateTimeField(default=basic_cms.utils.now_utc, verbose_name='creation date', editable=False)),
            ],
            options={
                'get_latest_by': 'creation_date',
                'verbose_name': 'content',
                'verbose_name_plural': 'contents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(default=basic_cms.utils.now_utc, verbose_name='creation date', editable=False)),
                ('publication_date', models.DateTimeField(help_text='When the page should go\n            live. Status must be "Published" for page to go live.', null=True, verbose_name='publication date', blank=True)),
                ('publication_end_date', models.DateTimeField(help_text='When to expire the page.\n            Leave empty to never expire.', null=True, verbose_name='publication end date', blank=True)),
                ('last_modification_date', models.DateTimeField(verbose_name='last modification date')),
                ('status', models.IntegerField(default=0, verbose_name='status', choices=[(1, 'Published'), (3, 'Hidden'), (0, 'Draft')])),
                ('template', models.CharField(max_length=100, null=True, verbose_name='template', blank=True)),
                ('delegate_to', models.CharField(max_length=100, null=True, verbose_name='delegate to', blank=True)),
                ('freeze_date', models.DateTimeField(help_text="Don't publish any content\n            after this date.", null=True, verbose_name='freeze date', blank=True)),
                ('redirect_to_url', models.CharField(max_length=200, null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('author', models.ForeignKey(related_name=b'pages', verbose_name='author', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(related_name=b'children', verbose_name='parent', blank=True, to='basic_cms.Page', null=True)),
                ('redirect_to', models.ForeignKey(related_name=b'redirected_pages', blank=True, to='basic_cms.Page', null=True)),
                ('sites', models.ManyToManyField(default=[1], help_text='The site(s) the page is accessible at.', verbose_name='sites', to='sites.Site', related_name=b'pages')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'get_latest_by': 'publication_date',
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
                'permissions': [('can_freeze', 'Can freeze page'), ('can_publish', 'Can publish page'), ('can_manage_en_gb', 'Manage Base'), ('can_manage_eng', 'Manage English')],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(unique=True, max_length=255)),
                ('page', models.ForeignKey(verbose_name='page', blank=True, to='basic_cms.Page', null=True)),
            ],
            options={
                'verbose_name_plural': 'Aliases',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='content',
            name='page',
            field=models.ForeignKey(verbose_name='page', to='basic_cms.Page'),
            preserve_default=True,
        ),
    ]
