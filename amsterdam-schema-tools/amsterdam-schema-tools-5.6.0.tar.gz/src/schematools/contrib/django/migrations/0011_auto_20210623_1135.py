# Generated by Django 3.1.12 on 2021-06-23 11:35

import django.utils.timezone
from django.contrib.postgres.fields import JSONField
from django.db import migrations, models
from django.db.models import F
from django.db.models.expressions import RawSQL
from django.db.models.functions import Cast

import schematools.contrib.django.validators


def set_defaults(apps, schema_editor) -> None:
    """Set non nullable field `path` to value of `id`.
    Has to use RawSql beqause F() does not support JSONfield.
    """
    Dataset = apps.get_model("datasets", "Dataset")
    Dataset.objects.all().update(path=RawSQL("schema_data ->> 'id'", ()))


class Migration(migrations.Migration):

    dependencies = [
        ("datasets", "0010_use_native_jsonfield"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dataset",
            name="url_prefix",
        ),
        migrations.AddField(
            model_name="dataset",
            name="path",
            field=models.TextField(
                null=True,
                validators=[schematools.contrib.django.validators.URLPathValidator()],
            ),
        ),
        migrations.RunPython(set_defaults),
        migrations.AlterField(
            model_name="dataset",
            name="path",
            field=models.TextField(
                unique=True,
                validators=[schematools.contrib.django.validators.URLPathValidator()],
            ),
        ),
    ]
