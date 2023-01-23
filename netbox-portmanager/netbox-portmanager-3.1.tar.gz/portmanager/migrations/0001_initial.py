# Generated by Django 4.1.5 on 2023-01-18 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import utilities.json


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('extras', '0084_staging'),
        ('dcim', '0167_module_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=80, unique=True)),
                ('description', models.CharField(default=None, max_length=80)),
                ('vlans', models.CharField(default='[]', max_length=300)),
                ('community_string', models.CharField(default='', max_length=80)),
                ('portsec_max', models.IntegerField(default=8)),
                ('devices', models.ManyToManyField(related_name='device_groups', to='dcim.device')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'Device Group',
                'verbose_name_plural': 'Device Groups',
            },
        ),
        migrations.CreateModel(
            name='ChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('component', models.CharField(editable=False, max_length=80)),
                ('before', models.CharField(editable=False, max_length=80)),
                ('after', models.CharField(editable=False, max_length=80)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Change Log',
                'verbose_name_plural': 'Changes Log',
                'ordering': ['-date'],
            },
        ),
    ]
