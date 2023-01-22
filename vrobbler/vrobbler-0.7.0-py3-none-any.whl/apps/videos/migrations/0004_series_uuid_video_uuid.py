# Generated by Django 4.1.5 on 2023-01-08 21:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_alter_video_run_time_ticks'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='uuid',
            field=models.UUIDField(
                blank=True, default=uuid.uuid4, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name='video',
            name='uuid',
            field=models.UUIDField(
                blank=True, default=uuid.uuid4, editable=False, null=True
            ),
        ),
    ]
