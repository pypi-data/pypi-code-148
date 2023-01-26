"""Модель ПО "Заявления на аттестацию"."""

from typing import List, Union
from uuid import uuid4

from pydantic.fields import Field
from pydantic.main import BaseModel


STATUS_PENDING = 'В очереди'


class Declaration(BaseModel):

    """Заявление."""

    id: str = Field(
        title='Уникальный ID',
        default_factory=lambda: str(uuid4())
    )
    stage: Union[str, None] = Field(
        title='Этап', default=None
    )
    status: str = Field(
        title='Статус', default=STATUS_PENDING
    )
    approved: Union[bool, None] = Field(
        title='Одобрено секретарём', default=False
    )
    rejected: Union[bool, None] = Field(
        title='Отклонено секретарём', default=False
    )
    needs_work: Union[bool, None] = Field(
        title='Требует доработки', default=False
    )
    withdrawn: Union[bool, None] = Field(
        title='Отозвано', default=False
    )
    experts: List[int] = Field(
        title='Эксперты', default_factory=list
    )


class Session(BaseModel):

    """Заседание."""

    declaration: Declaration = Field(title='Заявление')


class Comission(BaseModel):

    """Комиссия."""

    declaration: Declaration = Field(title='Заявление')


class Notification(BaseModel):

    """Уведомление."""

    declaration: Declaration = Field(title='Заявление')
