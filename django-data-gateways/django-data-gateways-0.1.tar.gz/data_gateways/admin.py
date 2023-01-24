from django.contrib import admin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.DataGateway)
class DataGatewayAdmin(admin.ModelAdmin):
    """Администрирование шлюзов данных"""

    list_display = ('name', 'description')
    list_display_links = ('name', )

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Проверка возможности добавление записей через амдинку"""
        return False

    def has_delete_permission(
        self, 
        request: HttpRequest, 
        obj: models.DataGateway | None = None,
    ) -> bool:
        """Проверка возможности удаления записей через амдинку"""
        return False


@admin.register(models.SenderModule)
class SenderModuleAdmin(admin.ModelAdmin):
    """Администрирование отправщиков данных"""

    list_display = ('name', 'description')
    list_display_links = ('name', )

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Проверка возможности добавление записей через амдинку"""
        return False

    def has_delete_permission(
        self, 
        request: HttpRequest, 
        obj: models.SenderModule | None = None,
    ) -> bool:
        """Проверка возможности удаления записей через амдинку"""
        return False

    def has_change_permission(
        self, 
        request: HttpRequest, 
        obj: models.SenderModule | None = None,
    ) -> bool:
        """Проверка возможности редактирования записей через амдинку"""
        return False


@admin.register(models.StrategyModule)
class StrategyModuleAdmin(admin.ModelAdmin):
    """Администрирование стратегий отправки"""

    list_display = ('name', 'description')
    list_display_links = ('name', )

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Проверка возможности добавление записей через амдинку"""
        return False

    def has_delete_permission(
        self, 
        request: HttpRequest, 
        obj: models.StrategyModule | None = None,
    ) -> bool:
        """Проверка возможности удаления записей через амдинку"""
        return False

    def has_change_permission(
        self, 
        request: HttpRequest, 
        obj: models.StrategyModule | None = None,
    ) -> bool:
        """Проверка возможности редактирования записей через амдинку"""
        return False


class StrategySenderRelationInline(admin.StackedInline):
    """Вложенная модель связи отправщика со стратегий для админки"""

    model = models.StrategySenderRelation
    extra = 0
    fk_name = 'parent_send_strategy'


@admin.register(models.StrategyConfig)
class StrategyConfigAdmin(admin.ModelAdmin):
    """Администрирование конфигураций стратегий отправки"""

    list_display = ('name', 'description')
    list_display_links = ('name', )
    inlines = (
        StrategySenderRelationInline,
    )


@admin.register(models.SenderConfig)
class SenderConfigAdmin(admin.ModelAdmin):
    """Администрирование конфигураций отправщиков"""

    list_display = ('name', 'description')
    list_display_links = ('name', )
