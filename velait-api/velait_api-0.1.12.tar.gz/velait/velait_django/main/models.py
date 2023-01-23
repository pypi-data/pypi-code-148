from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """ BaseModel should be added to every model """

    uuid = models.UUIDField(_("Идентификатор"), unique=True, default=uuid4, editable=False)
    is_deleted = models.BooleanField(_("Удалено ли?"), default=False)

    created_at = models.DateTimeField(_("дата создания"), auto_now_add=True)
    created_by_id = models.UUIDField(_("Создатель"), null=True)

    updated_at = models.DateTimeField(_("дата изменения"), auto_now=True)
    updated_by_id = models.UUIDField(_("Кто изменил"), null=True)

    ordering_fields = (
        'id',
        'uuid',
        'created',
        'modified',
    )

    searched_fields = (
        'id',
        'uuid',
        'created',
        'modified',
    )

    queryable_fields = ("id", "created_at", "updated_at", "created_by_id", "updated_by_id")
    orderable_fields = ("id", "created_at", "updated_at", "created_by_id", "updated_by_id")
    searchable_fields = ("id", "created_at", "updated_at", "created_by_id", "updated_by_id")
    searched_values = ("id", "created_at", "updated_at", "created_by_id", "updated_by_id")

    class Meta:
        abstract = True
