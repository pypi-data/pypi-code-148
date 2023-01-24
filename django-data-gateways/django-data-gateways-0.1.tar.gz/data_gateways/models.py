from django.db import models
from django.db.models import QuerySet
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .sending.senders import AbstractSender
from .sending.strategies import AbstractSendStrategy
from .utils.module_import import lazy_class_import
from .message_builder import AbstractMessageBuilder
from .sending.base_sendable_object import BaseSendableObject


def module_config_params_default() -> dict:
    """
    Функция получения дефолтных параметров для конфигурации.

    Используется для полей models.JSONField Django. Нужна именно 
    функция, чтобы каждый раз у нас были новые объекты класса dict.
    """

    return dict()


class Module(models.Model):
    """Абстрактна модель для хранения данных о модуле Python"""

    name = models.CharField(
        max_length=120,
        primary_key=True,
        verbose_name=_('Название'),
    )
    description = models.TextField(
        default='',
        blank=True,
        verbose_name=_('Описание'),
    )
    module_path = models.CharField(
        max_length=512,
        unique=True,
        verbose_name=_('Модуль'),
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self._meta.verbose_name}: {self.name}'


class SenderModule(Module):
    """Модель отправщика"""

    class Meta:
        verbose_name = _('Отправщик данных')
        verbose_name_plural = _('Отправщики данных')


class StrategyModule(Module):
    """Модель стратегии отправки"""

    class Meta:
        verbose_name = _('Стратегия отправки')
        verbose_name_plural = _('Стратегии отправки')


class ModuleConfig(models.Model):
    """Абстрактная модель конфигурации модуля"""

    name = models.CharField(
        max_length=120,
        primary_key=True,
        verbose_name=_('Название'),
    )
    description = models.TextField(
        default='',
        blank=True,
        verbose_name=_('Описание'),
    )
    module = models.ForeignKey(
        to=Module,
        on_delete=models.CASCADE,
        related_name='configs',
        related_query_name='config',
    )
    init_params = models.JSONField(
        blank=True,
        default=module_config_params_default,
        verbose_name=_('Параметры'),
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self._meta.verbose_name}: {self.name}'


class SenderConfig(ModuleConfig):
    """Модель конфигурации отправщика сообщений"""

    module = models.ForeignKey(
        to=SenderModule,
        on_delete=models.CASCADE,
        related_name='sender_configs',
        related_query_name='sender_config',
        verbose_name=_('Отправщик'),
    )

    def get_configured_module(self) -> AbstractSender:
        """Получение инициализированного отправщика"""

        return lazy_class_import(self.module.module_path)(**self.init_params)

    class Meta:
        verbose_name = _('Конфигурация отправщика')
        verbose_name_plural = _('Конфигурации отправщиков')


class StrategyConfig(ModuleConfig):
    """Модель конфигурации стратегии отправки"""

    module = models.ForeignKey(
        to=StrategyModule,
        on_delete=models.CASCADE,
        related_name='strategy_configs',
        related_query_name='strategy_config',
        verbose_name=_('Стратегия отправки'),
    )

    def get_configured_module(self) -> AbstractSendStrategy:
        """Получение инициализированного отправщика"""

        return lazy_class_import(self.module.module_path)(**self.init_params)

    class Meta:
        verbose_name = _('Конфигурация стратегии отправки')
        verbose_name_plural = _('Конфигурации стратегий отправки')


class StrategySenderRelation(models.Model):
    """Модель связи между конфигурацией стратегии и конфигурацией отправщиков"""

    parent_send_strategy = models.ForeignKey(
        to=StrategyConfig,
        on_delete=models.CASCADE,
        related_name='senders',
        related_query_name='sender',
        verbose_name=_('Родителькая стратегия отправки'),
    ) 
    serial_number = models.PositiveSmallIntegerField(
        verbose_name=_('Порядковый номер'),
    )
    enabled = models.BooleanField(
        default=True,
        verbose_name=_('Активен'),
    )

    # TODO: Поля sender_config и send_strategy_config можно заменить GenericField 
    #   полем Django, однако для этого, вероятнее всего, придется как минимум 
    #   сделать кастомную форму для отображения в админке.
    sender_config = models.ForeignKey(
        to=SenderConfig,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sender_relations',
        related_query_name='sender_relation',
        verbose_name=_('Отправщик данных'),
    )
    send_strategy_config = models.ForeignKey(
        to=StrategyConfig,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='strategy_relations',
        related_query_name='strategy_relation',
        verbose_name=_('Стратегия отправки данных'),
    )

    class Meta:
        verbose_name = _('Связь с отправщиком')
        verbose_name_plural = _('Связи с отправщиками')
        unique_together = ('serial_number', 'parent_send_strategy')
        ordering = ('serial_number', )

    def clean(self) -> None:
        """Общая валидация модели"""

        errors: dict[str, ValidationError] = {}

        # Проверяем, чтобы было выбрано только одно значение: либо отправщик, либо стратегия.
        if not (bool(self.sender_config) ^ bool(self.send_strategy_config)):
            message_error = 'Необходимо выбрать либо отправщик, либо стратегию'
            errors['sender_config'] = message_error
            errors['send_strategy_config'] = message_error

        # Проверка, чтобы стратегия не ссылалась сама на себя. Иначе будет бесконечная 
        # отправка сообщений.
        if self.parent_send_strategy_id == self.send_strategy_config_id:
            errors['send_strategy_config'] = 'Стратегия не может ссылаться сама на себя'

        if errors:
            raise ValidationError(errors)

    def get_module_config(self) -> ModuleConfig | None:
        """
        Получение конфигурации отправщика/стратегии отправки.

        Объект может содержать данные о модуле либо класса отправщика, 
        либо класса стратегии отправки.

        :return: Объект конфигурации отправщика/стратегии отправки.
        """

        return self.sender_config or self.send_strategy_config

    def __str__(self) -> str:
        return f'{self.parent_send_strategy.name}#{self.get_module_config()}'


class WithModuleDataGatewayManager(models.Manager):
    """
    Класс менеджера записей для модели `DataGateway` с 
    оптимизированным запросом.

    Делает JOIN'ы (select_related'ы) для моделей конфигурации стратегии 
    и модуля стратегии.
    """

    def get_queryset(self) -> QuerySet['DataGateway']:
        """
        Получение набора записей с данными о конфигурации 
        стратегии и модуле.
        """

        return super().get_queryset().select_related(
            'send_strategy', 
            'send_strategy__module',
        )


class DataGateway(models.Model):
    """Модель шлюза данных"""

    name = models.CharField(
        max_length=120,
        unique=True,
        verbose_name=_('Название шлюза'),
    )
    description = models.TextField(
        default='',
        blank=True,
        verbose_name=_('Описание'),
    )
    send_strategy = models.ForeignKey(
        to=StrategyConfig,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='data_gateways',
        related_query_name='data_gateway',
        verbose_name=_('Стратегия отправки'),
    )

    objects = models.Manager()
    with_module = WithModuleDataGatewayManager()

    class Meta:
        verbose_name = _('Шлюз данных')
        verbose_name_plural = _('Шлюзы данных')

    def get_sender(
        self,
        message_builder: AbstractMessageBuilder | None = None,
        subject_template: str | None = None,
        body_template: str | None = None,
    ) -> BaseSendableObject:
        """
        Метод инициализации и конфигурации объекта, готового к отправке данных 
        согласено стратегии и всем настройкам вложенных отправщиков и стратегий.

        :param message_builder: 
            Объект билдера сообщения на основе данных. Если None, 
            используется дефолтный билдер сообщений.
        :param subject_template:
            Путь до шаблона темы сообщения. Нужен, если не передан параметр message_builder.
            Если message_builder передан, параметр игнорируется.
        :param body_template: 
            Путь до шаблона тела сообщения. Нужен, если не передан параметр message_builder.
            Если message_builder передан, параметр игнорируется.
        
        :return: Объект отправщика.
        """

        # TODO: Здесь мы имеем дело со структурой данных "Дерево".
        # Главная стратегия - корень дерева, связи стратегии и остальных 
        # отправщиков - листы дерева.
        # Мы должны получать в запросе все листы текущей стратегии, итерироваться 
        # по ним. Если обычный отправщик - инициализируем его и сохраняем в список. 
        # Если стратегия - сначала рекурсивно вызываем эту же функцию инициализации 
        # стратегии, но для новой стратегии, а потом уже эту стратегию также добавляем 
        # в список и этот список передаем в параметр sanders главной стратегии.

        # if self.send_strategy:
        #     ...
        # else:
        #     # TODO: Добавить возможность выбора в шлюзе данных обычного сендера.
        #     ...

        return self.__load_strategy(
            self.send_strategy,
            message_builder,
            subject_template,
            body_template,
        )

    def __load_strategy(
        self, 
        strategy_config_model: StrategyConfig,
        message_builder: AbstractMessageBuilder | None = None,
        subject_template: str | None = None,
        body_template: str | None = None,
    ) -> AbstractSendStrategy:
        """Метод загрузки объекта стратегии со всеми отправщиками"""

        # Получаем у текущей модели конфигурации стратегии все настройки отправщиков.
        # Для оптимизации запросов к БД делаем JOIN'ы.
        strategy_sender_relations: list[StrategySenderRelation] = list(
            strategy_config_model.senders.select_related(
                'send_strategy_config', 
                'sender_config',
                'send_strategy_config__module',
                'sender_config__module',
            ).all()
        )

        # Создаем список ISendable объектов для текущей стратегии.
        senders_for_strategy: list[BaseSendableObject] = []
        for relation in strategy_sender_relations:
            # Если настройка отправщика у текущей стратегии выключена, 
            # то пропускаем текущий отправщик.
            if not relation.enabled:
                continue

            # Если в текущей настройке находится вложенная стратегия отправки, 
            # рекурсивно вызываем для нее выгрузку стратегии и добавляем ее в 
            # текущий список отправщиков для текущей стратегии.
            if relation.send_strategy_config:
                new_strategy = self.__load_strategy(
                    strategy_config_model=relation.send_strategy_config,
                    message_builder=message_builder,
                    subject_template=subject_template,
                    body_template=body_template,
                )
                senders_for_strategy.append(new_strategy)
            # Иначе загружаем обычный отправщик.
            else:
                module_path = relation.sender_config.module.module_path
                init_params: dict = relation.sender_config.init_params
                new_sender: AbstractSender = lazy_class_import(module_path)(
                    message_builder=message_builder,
                    subject_template=subject_template,
                    body_template=body_template,
                    **init_params,
                )
                senders_for_strategy.append(new_sender)

        # Создаем объект текущей стратегии и инициализируем его рекурсивно 
        # выгруженными отправщиками и другими параметрами.
        current_strategy_object: AbstractSendStrategy = \
            lazy_class_import(strategy_config_model.module.module_path)(
                senders=senders_for_strategy,
                **strategy_config_model.init_params,
            )

        return current_strategy_object

    def __str__(self) -> str:
        return f'{self._meta.verbose_name}: {self.name}'
