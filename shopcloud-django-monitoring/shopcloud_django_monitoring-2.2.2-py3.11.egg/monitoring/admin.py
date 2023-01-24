from django.contrib import admin
from django.contrib.admin import register

from . import models


@register(models.Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'code',
        'type',
        'created_at',
    )
    readonly_fields = (
        'id',
        'updated_at',
        'created_at',
    )


def metric_proceed(modeladmin, request, queryset):
    for obj in queryset:
        models.Metric.fire_event_proceed(models.Metric.__name__, obj.id)


metric_proceed.short_description = 'PROCEED'


@register(models.Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'code',
        'source',
        'is_active',
        'last_run_at',
        'value',
        'value_min',
        'value_max',
        'is_ok',
        'created_at',
    )
    list_select_related = (
        'source',
    )
    readonly_fields = (
        'id',
        'value',
        'is_ok',
        'last_run_at',
        'updated_at',
        'created_at',
    )
    list_filter = (
        'is_active',
        'is_ok',
    )
    search_fields = (
        '=id',
        'name',
        'code',
    )
    actions = (
        metric_proceed,
    )
