# Generated by Django 4.1.5 on 2023-01-04 21:33

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created',
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name='created'
                    ),
                ),
                (
                    'modified',
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name='modified'
                    ),
                ),
                ('name', models.CharField(max_length=255)),
                ('overview', models.TextField(blank=True, null=True)),
                ('tagline', models.TextField(blank=True, null=True)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created',
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name='created'
                    ),
                ),
                (
                    'modified',
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name='modified'
                    ),
                ),
                (
                    'video_type',
                    models.CharField(
                        choices=[
                            ('U', 'Unknown'),
                            ('E', 'TV Episode'),
                            ('M', 'Movie'),
                        ],
                        default='U',
                        max_length=1,
                    ),
                ),
                (
                    'title',
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ('overview', models.TextField(blank=True, null=True)),
                ('tagline', models.TextField(blank=True, null=True)),
                (
                    'run_time',
                    models.CharField(blank=True, max_length=8, null=True),
                ),
                (
                    'run_time_ticks',
                    models.BigIntegerField(blank=True, null=True),
                ),
                ('year', models.IntegerField()),
                ('season_number', models.IntegerField(blank=True, null=True)),
                ('episode_number', models.IntegerField(blank=True, null=True)),
                (
                    'tvdb_id',
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    'imdb_id',
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    'tvrage_id',
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    'tv_series',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to='videos.series',
                    ),
                ),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
