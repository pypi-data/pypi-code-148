"""Модель взаимодействия с платформой Camunda."""

# pylint: disable=C0103

from datetime import date
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic.main import BaseModel
from pydantic.networks import AnyUrl


TYPE_MAP = {
    str: 'String',
    bool: 'Boolean',
    int: 'Integer',
    float: 'Double',
    date: 'Date',
    type(None): 'Null'
}

REVERSE_MAP = {
    val: key
    for (key, val) in TYPE_MAP.items()
}


class Deployment(BaseModel):

    """Данные о развёртывании процесса."""

    id: str
    name: Optional[str] = None
    source: Optional[str] = None
    tenantId: Optional[str] = None
    deploymentTime: str

    deployedProcessDefinitions: Optional[Dict[str, 'Definition']] = {}
    deployedDecisionDefinitions: Optional[Dict[str, Any]] = {}
    deployedDecisionRequirementsDefinitions: Optional[Dict[str, Any]] = {}


class Definition(BaseModel):

    """Определение процесса."""

    key: str
    id: str
    name: str
    deploymentId: UUID
    version: int

    startableInTasklist: bool = False
    suspended: bool = False
    tenantId: Optional[str] = None

    versionTag: Optional[str] = None
    description: Optional[str] = None
    resource: Optional[str] = None
    category: AnyUrl
    diagram: Optional[str] = None
    historyTimeToLive: Optional[int] = None


class Process(BaseModel):

    """Запущенный процесс."""

    id: str
    definitionId: str
    businessKey: Optional[str] = None
    caseInstanceId: Optional[str] = None
    ended: bool = False
    suspended: bool = False
    tenantId: Optional[str] = None


class Topic(BaseModel):

    """Топик для подписки обработчиков."""

    name: str

    class Config:
        frozen = True


class Variable(BaseModel):

    """Переменная задачи, сообщения."""

    type: str
    value: Union[str, bool, int, float, date, None]  # См. TYPE_MAP
    valueInfo: dict = {}

    def __init__(self, *args, **kwargs):
        kwargs['type'] = TYPE_MAP[type(kwargs['value'])]
        super().__init__(*args, **kwargs)


Variables = Dict[str, Variable]
"""Переменные задач, сообщений."""


class ExternalTask(BaseModel):

    """Внешняя задача.

    Считается внешней по отн. к Camunda, исполняется воркером или
    отдельным приложением.
    """

    id: str
    topicName: str
    businessKey: Optional[str] = None

    processDefinitionId: str
    processDefinitionKey: str
    processDefinitionVersionTag: Optional[str] = None

    processInstanceId: str

    activityId: str
    activityInstanceId: str
    executionId: str

    variables: Variables = {}

    errorMessage: Optional[str] = None

    lockExpirationTime: Optional[str] = None
    retries: Optional[int] = None
    suspended: bool = False
    workerId: Optional[str] = None
    tenantId: Optional[str] = None
    priority: Optional[int] = None
    extensionProperties: dict = {}

    topic: Topic

    def __init__(self, *args, **kwargs):
        topic = Topic(name=kwargs['topicName'])
        super().__init__(*args, topic=topic, **kwargs)


class Message(BaseModel):

    """Сообщение.

    Может использоваться как возникающее событие.
    """

    messageName: str
    businessKey: str
    resultEnabled: Optional[bool] = True
    variablesInResultEnabled: Optional[bool] = True
    correlationKeys: Variables = {}
    processVariables: Variables = {}


class Execution(BaseModel):

    """Среда исполнения процесса."""

    id: str
    processInstanceId: str
    ended: bool
    tenantId: Union[str, None] = None


class MessageResult(BaseModel):

    """Результат отправки сообщения."""

    resultType: str
    execution: Optional[Union[Execution, None]] = None
    processInstance: Optional[Process] = None
    variables: Variables = {}


class ErrorDetail(BaseModel):

    """Детальная информация об ошибке."""

    column: int
    line: int
    mainElementId: str
    message: str
    elementIds: List[str]


TWarning = Any


class MessageDetail(BaseModel):

    """Детальная информация сообщения."""

    errors: List[ErrorDetail]
    warnings: List[TWarning]


TMessageDetails = Dict[str, MessageDetail]


class Error(BaseModel):

    """Ошибка запроса."""

    type: str
    message: str
    code: int = 0
    details: Optional[TMessageDetails] = None


Deployment.update_forward_refs()
