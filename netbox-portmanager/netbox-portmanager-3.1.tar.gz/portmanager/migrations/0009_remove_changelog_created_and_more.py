# Generated by Django 4.1.5 on 2023-01-21 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portmanager', '0008_changelog_interface'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='changelog',
            name='created',
        ),
        migrations.RemoveField(
            model_name='changelog',
            name='custom_field_data',
        ),
        migrations.RemoveField(
            model_name='changelog',
            name='last_updated',
        ),
        migrations.RemoveField(
            model_name='changelog',
            name='tags',
        ),
    ]
