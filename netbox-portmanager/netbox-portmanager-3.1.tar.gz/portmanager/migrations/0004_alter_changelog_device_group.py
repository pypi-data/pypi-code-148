# Generated by Django 4.1.5 on 2023-01-18 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portmanager', '0003_changelog_device_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changelog',
            name='device_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='portmanager.devicegroup'),
        ),
    ]
