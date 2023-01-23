# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybotx',
 'pybotx.bot',
 'pybotx.bot.api',
 'pybotx.bot.api.responses',
 'pybotx.bot.callbacks',
 'pybotx.bot.middlewares',
 'pybotx.client',
 'pybotx.client.bots_api',
 'pybotx.client.chats_api',
 'pybotx.client.events_api',
 'pybotx.client.exceptions',
 'pybotx.client.files_api',
 'pybotx.client.notifications_api',
 'pybotx.client.smartapps_api',
 'pybotx.client.stickers_api',
 'pybotx.client.users_api',
 'pybotx.models',
 'pybotx.models.message',
 'pybotx.models.system_events']

package_data = \
{'': ['*']}

install_requires = \
['aiocsv>=1.2.3,<1.3.0',
 'aiofiles>=0.7.0,<0.9.0',
 'httpx==0.23.0',
 'loguru>=0.6.0,<0.7.0',
 'mypy-extensions>=0.2.0,<0.5.0',
 'pydantic>=1.6.0,<1.11.0',
 'typing-extensions>=3.7.4,<5.0.0']

setup_kwargs = {
    'name': 'pybotx',
    'version': '0.53.2',
    'description': 'A python library for interacting with eXpress BotX API',
    'long_description': '# pybotx\n\n*Библиотека для создания чат-ботов и SmartApps для мессенджера eXpress*\n\n[![PyPI version](https://badge.fury.io/py/botx.svg)](https://badge.fury.io/py/pybotx)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybotx)\n[![Coverage](https://codecov.io/gh/ExpressApp/pybotx/branch/master/graph/badge.svg)](https://codecov.io/gh/ExpressApp/pybotx/branch/master)\n[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n\n## Особенности\n\n* Простая для использования\n* Поддерживает коллбэки BotX\n* Легко интегрируется с асинхронными веб-фреймворками\n* Полное покрытие тестами\n* Полное покрытие аннотациями типов\n\n\n## Установка\n\nИспользуя `poetry`:\n\n```bash\npoetry add pybotx\n```\n\n**Предупреждение:** Данный проект находится в активной разработке (`0.y.z`) и\nего API может быть изменён при повышении минорной версии.\n\n\n## Информация о мессенджере eXpress и платформе BotX\n\nДокументацию по мессенджеру (включая руководство пользователя и администратора)\nможно найти на [официальном сайте](https://express.ms/).\n\nПеред тем, как продолжать знакомство с библиотекой `pybotx`,\nсоветуем прочитать данные статьи: [Что такое чат-боты и SmartApp\n](https://ccsteam.atlassian.net/wiki/spaces/SMARTAPP/pages/311001089)\nи [Взаимодействие с Bot API и BotX API\n](https://ccsteam.atlassian.net/wiki/spaces/SMARTAPP/pages/311001185).\nВ этих статьях находятся исчерпывающие примеры работы с платформой, которые\nлегко повторить, используя `pybotx`.\n\nТакже не будет лишним ознакомиться с [документацией по плаформе BotX\n](https://hackmd.ccsteam.ru/s/botx_platform).\n\n\n## Примеры готовых проектов на базе pybotx\n\n* [Next Feature Bot](https://github.com/ExpressApp/next-feature-bot) - бот,\n  используемый для тестирования функционала платформы BotX.\n* [ToDo Bot](https://github.com/ExpressApp/todo-bot) - бот для ведения списка\n  дел.\n* [Weather SmartApp](https://github.com/ExpressApp/weather-smartapp) -\n  приложение для просмотра погоды.\n\n\n## Минимальный пример бота (интеграция с FastAPI)\n\n```python\nfrom http import HTTPStatus\nfrom uuid import UUID\n\nfrom fastapi import FastAPI, Request\nfrom fastapi.responses import JSONResponse\n\n# В этом и последующих примерах импорт из `pybotx` будет производиться\n# через звёздочку для краткости. Однако, это не является хорошей практикой.\nfrom pybotx import *\n\ncollector = HandlerCollector()\n\n\n@collector.command("/echo", description="Send back the received message body")\nasync def echo_handler(message: IncomingMessage, bot: Bot) -> None:\n    await bot.answer_message(message.body)\n\n\n# Сюда можно добавлять свои обработчики команд\n# или копировать примеры кода, расположенные ниже.\n\n\nbot = Bot(\n    collectors=[collector],\n    bot_accounts=[\n        BotAccountWithSecret(\n            # Не забудьте заменить эти учётные данные на настоящие,\n            # когда создадите бота в панели администратора.\n            id=UUID("123e4567-e89b-12d3-a456-426655440000"),\n            host="cts.example.com",\n            secret_key="e29b417773f2feab9dac143ee3da20c5",\n        ),\n    ],\n)\n\napp = FastAPI()\napp.add_event_handler("startup", bot.startup)\napp.add_event_handler("shutdown", bot.shutdown)\n\n\n# На этот эндпоинт приходят команды BotX\n# (сообщения и системные события).\n@app.post("/command")\nasync def command_handler(request: Request) -> JSONResponse:\n    bot.async_execute_raw_bot_command(await request.json())\n    return JSONResponse(\n        build_command_accepted_response(),\n        status_code=HTTPStatus.ACCEPTED,\n    )\n\n\n# К этому эндпоинту BotX обращается, чтобы узнать\n# доступность бота и его список команд.\n@app.get("/status")\nasync def status_handler(request: Request) -> JSONResponse:\n    status = await bot.raw_get_status(dict(request.query_params))\n    return JSONResponse(status)\n\n\n# На этот эндпоинт приходят коллбэки с результатами\n# выполнения асинхронных методов в BotX.\n@app.post("/notification/callback")\nasync def callback_handler(request: Request) -> JSONResponse:\n    await bot.set_raw_botx_method_result(await request.json())\n    return JSONResponse(\n        build_command_accepted_response(),\n        status_code=HTTPStatus.ACCEPTED,\n    )\n```\n\n## Примеры\n\n\n### Получение сообщений\n\n*([подробное описание функции](\nhttps://ccsteam.atlassian.net/wiki/spaces/SMARTAPP/pages/311001185/Bot+API+BotX+API#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D0%B9/%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%BD%D1%8B%D1%85-%D1%81%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D0%B9))*\n\n```python\nfrom uuid import UUID\n\nfrom pybotx import *\n\nADMIN_HUIDS = (UUID("123e4567-e89b-12d3-a456-426614174000"),)\n\ncollector = HandlerCollector()\n\n\n@collector.command("/visible", description="Visible command")\nasync def visible_handler(_: IncomingMessage, bot: Bot) -> None:\n    # Обработчик команды бота. Команда видимая, поэтому описание\n    # является обязательным.\n    print("Hello from `/visible` handler")\n\n\n@collector.command("/_invisible", visible=False)\nasync def invisible_handler(_: IncomingMessage, bot: Bot) -> None:\n    # Невидимая команда - не отображается в списке команд бота\n    # и не нуждается в описании.\n    print("Hello from `/invisible` handler")\n\n\nasync def is_admin(status_recipient: StatusRecipient, bot: Bot) -> bool:\n    return status_recipient.huid in ADMIN_HUIDS\n\n\n@collector.command("/admin-command", visible=is_admin)\nasync def admin_command_handler(_: IncomingMessage, bot: Bot) -> None:\n    # Команда показывается только если пользователь является админом.\n    # Список команд запрашивается при открытии чата в приложении.\n    print("Hello from `/admin-command` handler")\n\n\n@collector.default_message_handler\nasync def default_handler(_: IncomingMessage, bot: Bot) -> None:\n    # Если команда не была найдена, вызывается `default_message_handler`,\n    # если он определён. Такой обработчик может быть только один.\n    print("Hello from default handler")\n```\n\n\n### Получение системных событий\n\n*([подробное описание функции](\nhttps://ccsteam.atlassian.net/wiki/spaces/SMARTAPP/pages/311001185/Bot+API+BotX+API#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D0%B9/%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%BD%D1%8B%D1%85-%D1%81%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D0%B9))*\n\n```python\nfrom pybotx import *\n\ncollector = HandlerCollector()\n\n\n@collector.chat_created\nasync def chat_created_handler(event: ChatCreatedEvent, bot: Bot) -> None:\n    # Работа с событиями производится с помощью специальных обработчиков.\n    # На каждое событие можно объявить только один такой обработчик.\n    print(f"Got `chat_created` event: {event}")\n\n\n@collector.smartapp_event\nasync def smartapp_event_handler(event: SmartAppEvent, bot: Bot) -> None:\n    print(f"Got `smartapp_event` event: {event}")\n```\n\n\n### Middlewares\n\n*(Этот функционал относится исключительно к `pybotx`)*\n\n```python\nfrom httpx import AsyncClient\n\nfrom pybotx import *\n\ncollector = HandlerCollector()\n\n\nasync def custom_api_client_middleware(\n    message: IncomingMessage,\n    bot: Bot,\n    call_next: IncomingMessageHandlerFunc,\n) -> None:\n    # До вызова `call_next` (обязателен в каждой миддлвари) располагается\n    # код, который выполняется до того, как сообщение дойдёт до\n    # своего обработчика.\n    async_client = AsyncClient()\n\n    # У сообщения есть объект состояния, в который миддлвари могут добавлять\n    # необходимые данные.\n    message.state.async_client = async_client\n\n    await call_next(message, bot)\n\n    # После вызова `call_next` выполняется код, когда обработчик уже\n    # завершил свою работу.\n    await async_client.aclose()\n\n\n@collector.command(\n    "/fetch-resource",\n    description="Fetch resource from passed URL",\n    middlewares=[custom_api_client_middleware],\n)\nasync def fetch_resource_handler(message: IncomingMessage, bot: Bot) -> None:\n    async_client = message.state.async_client\n    response = await async_client.get(message.argument)\n    print(response.status_code)\n```\n\n### Сборщики обработчиков\n\n*(Этот функционал относится исключительно к `pybotx`)*\n\n```python\nfrom uuid import UUID, uuid4\n\nfrom pybotx import *\n\nADMIN_HUIDS = (UUID("123e4567-e89b-12d3-a456-426614174000"),)\n\n\nasync def request_id_middleware(\n    message: IncomingMessage,\n    bot: Bot,\n    call_next: IncomingMessageHandlerFunc,\n) -> None:\n    message.state.request_id = uuid4()\n    await call_next(message, bot)\n\n\nasync def ensure_admin_middleware(\n    message: IncomingMessage,\n    bot: Bot,\n    call_next: IncomingMessageHandlerFunc,\n) -> None:\n    if message.sender.huid not in ADMIN_HUIDS:\n        await bot.answer_message("You are not admin")\n        return\n\n    await call_next(message, bot)\n\n\n# Для того чтобы добавить новый обработчик команды,\n# необходимо создать экземпляр класса `HandlerCollector`.\n# Позже этот сборщик будет использован при создании бота.\nmain_collector = HandlerCollector(middlewares=[request_id_middleware])\n\n# У сборщиков (как у обработчиков), могут быть собственные миддлвари.\n# Они автоматически применяются ко всем обработчикам данного сборщика.\nadmin_collector = HandlerCollector(middlewares=[ensure_admin_middleware])\n\n# Сборщики можно включать друг в друга. В данном примере у\n# `admin_collector` будут две миддлвари. Первая - его собственная,\n# вторая - полученная при включении в `main_collector`.\nmain_collector.include(admin_collector)\n```\n\n\n### Отправка сообщения\n\n*([подробное описание функции](\nhttps://ccsteam.atlassian.net/wiki/spaces/SMARTAPP/pages/311001185/Bot+API+BotX+API#%D0%9E%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D1%8F))*\n\n```python\nfrom uuid import UUID\n\nfrom pybotx import *\n\ncollector = HandlerCollector()\n\n\n@collector.command("/answer", description="Answer to sender")\nasync def answer_to_sender_handler(message: IncomingMessage, bot: Bot) -> None:\n    # Т.к. нам известно, откуда пришло сообщение, у `pybotx` есть необходимый\n    # контекст для отправки ответа.\n    await bot.answer_message("Text")\n\n\n@collector.command("/send", description="Send message to specified chat")\nasync def send_message_handler(message: IncomingMessage, bot: Bot) -> None:\n    try:\n        chat_id = UUID(message.argument)\n    except ValueError:\n        await bot.answer_message("Invalid chat id")\n        return\n\n    # В данном случае нас интересует не ответ, а отправка сообщения\n    # в другой чат. Чат должен существовать и бот должен быть в нём.\n    try:\n        await bot.send_message(\n            bot_id=message.bot.id,\n            chat_id=chat_id,\n            body="Text",\n        )\n    except Exception as exc:\n        await bot.answer_message(f"Error: {exc}")\n        return\n\n    await bot.answer_message("Message was send")\n\n\n@collector.command("/prebuild-answer", description="Answer with prebuild message")\nasync def prebuild_answer_handler(message: IncomingMessage, bot: Bot) -> None:\n    # С помощью OutgoingMessage можно выносить логику\n    # формирования ответов в другие модули.\n    answer = OutgoingMessage(\n        bot_id=message.bot.id,\n        chat_id=message.chat.id,\n        body="Text",\n    )\n    await bot.send(message=answer)\n```\n\n\n#### Отправка сообщения с кнопками\n\n*([подробное описание функции](\nhttps://ccsteam.atlassian.net/wiki/spaces/SMARTAPP/pages/311001185/Bot+API+BotX+API#%D0%9E%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D1%8F-%D1%81-%D0%BA%D0%BD%D0%BE%D0%BF%D0%BA%D0%B0%D0%BC%D0%B8))*\n\n```python\nfrom pybotx import *\n\ncollector = HandlerCollector()\n\n\n@collector.command("/bubbles", description="Send buttons")\nasync def bubbles_handler(message: IncomingMessage, bot: Bot) -> None:\n    # Если вам нужна клавиатура под полем для ввода сообщения,\n    # используйте `KeyboardMarkup`. Этот класс имеет те же методы,\n    # что и `BubbleMarkup`.\n    bubbles = BubbleMarkup()\n    bubbles.add_button(\n        command="/choose",\n        label="Red",\n        data={"pill": "red"},\n    )\n    bubbles.add_button(\n        command="/choose",\n        label="Blue",\n        data={"pill": "blue"},\n        new_row=False,\n    )\n\n    await bot.answer_message(\n        "The time has come to make a choice, Mr. Anderson:",\n        bubbles=bubbles,\n    )\n```\n\n\n#### Упоминание пользователя\n\n*([подробное описание функции](\nhttps://ccsteam.atlassian.net/wiki/spaces/SMARTAPP/pages/311001185/Bot+API+BotX+API#%D0%A3%D0%BF%D0%BE%D0%BC%D0%B8%D0%BD%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F))*\n\n```python\nfrom pybotx import *\n\ncollector = HandlerCollector()\n\n\n@collector.command("/send-contact", description="Send author\'s contact")\nasync def send_contact_handler(message: IncomingMessage, bot: Bot) -> None:\n    contact = MentionBuilder.contact(message.sender.huid)\n    await bot.answer_message(f"Author is {contact}")\n\n\n@collector.command("/echo-contacts", description="Send back recieved contacts")\nasync def echo_contact_handler(message: IncomingMessage, bot: Bot) -> None:\n    if not (contacts := message.mentions.contacts):\n        await bot.answer_message("Please send at least one contact")\n        return\n\n    answer = ", ".join(map(str, contacts))\n    await bot.answer_message(answer)\n```\n\n\n#### Отправка файла в сообщении\n\n*([подробное описание функции](\nhttps://ccsteam.atlassian.net/wiki/spaces/SMARTAPP/pages/311001185/Bot+API+BotX+API#%D0%9E%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0-%D1%84%D0%B0%D0%B9%D0%BB%D0%B0-%D0%B2-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D0%B8))*\n\n```python\nfrom aiofiles.tempfile import NamedTemporaryFile\n\nfrom pybotx import *\n\ncollector = HandlerCollector()\n\n\n@collector.command("/send-file", description="Send file")\nasync def send_file_handler(message: IncomingMessage, bot: Bot) -> None:\n    # Для создания файла используется file-like object\n    # с поддержкой асинхронных операций.\n    async with NamedTemporaryFile("wb+") as async_buffer:\n        await async_buffer.write(b"Hello, world!\\n")\n        await async_buffer.seek(0)\n\n        file = await OutgoingAttachment.from_async_buffer(async_buffer, "test.txt")\n\n    await bot.answer_message("Attached file", file=file)\n\n\n@collector.command("/echo-file", description="Echo file")\nasync def echo_file_handler(message: IncomingMessage, bot: Bot) -> None:\n    if not (attached_file := message.file):\n        await bot.answer_message("Attached file is required")\n        return\n\n    await bot.answer_message("", file=attached_file)\n```\n\n\n### Редактирование сообщения\n\n*([подробное описание функции](\nhttps://hackmd.ccsteam.ru/s/E9MPeOxjP#%D0%A0%D0%B5%D0%B4%D0%B0%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D1%81%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D1%8F))*\n\n```python\nfrom pybotx import *\n\ncollector = HandlerCollector()\n\n\n@collector.command("/increment", description="Self-updating widget")\nasync def increment_handler(message: IncomingMessage, bot: Bot) -> None:\n    if message.source_sync_id:  # ID сообщения, в котором была нажата кнопка.\n        current_value = message.data["current_value"]\n        next_value = current_value + 1\n    else:\n        current_value = 0\n        next_value = 1\n\n    answer_text = f"Counter: {current_value}"\n    bubbles = BubbleMarkup()\n    bubbles.add_button(\n        command="/increment",\n        label="+",\n        data={"current_value": next_value},\n    )\n\n    if message.source_sync_id:\n        await bot.edit_message(\n            bot_id=message.bot.id,\n            sync_id=message.source_sync_id,\n            body=answer_text,\n            bubbles=bubbles,\n        )\n    else:\n        await bot.answer_message(answer_text, bubbles=bubbles)\n```\n\n\n### Обработчики ошибок\n\n*(Этот функционал относится исключительно к `pybotx`)*\n\n```python\nfrom loguru import logger\n\nfrom pybotx import *\n\n\nasync def internal_error_handler(\n    message: IncomingMessage,\n    bot: Bot,\n    exc: Exception,\n) -> None:\n    logger.exception("Internal error:")\n\n    await bot.answer_message(\n        "**Error:** internal error, please contact your system administrator",\n    )\n\n\n# Для перехвата исключений существуют специальные обработчики.\n# Бот принимает словарь из типов исключений и их обработчиков.\nbot = Bot(\n    collectors=[],\n    bot_accounts=[],\n    exception_handlers={Exception: internal_error_handler},\n)\n```\n\n### Создание чата\n\n*([подробное описание функции](\nhttps://ccsteam.atlassian.net/wiki/spaces/SMARTAPP/pages/311001185/Bot+API+BotX+API#%D0%A1%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5-%D1%87%D0%B0%D1%82%D0%B0))*\n\n```python\nfrom pybotx import *\n\ncollector = HandlerCollector()\n\n\n@collector.command("/create-group-chat", description="Create group chat")\nasync def create_group_chat_handler(message: IncomingMessage, bot: Bot) -> None:\n    if not (contacts := message.mentions.contacts):\n        await bot.answer_message("Please send at least one contact")\n        return\n\n    try:\n        chat_id = await bot.create_chat(\n            bot_id=message.bot.id,\n            name="New group chat",\n            chat_type=ChatTypes.GROUP_CHAT,\n            huids=[contact.entity_id for contact in contacts],\n        )\n    except (ChatCreationProhibitedError, ChatCreationError) as exc:\n        await bot.answer_message(str(exc))\n        return\n\n    chat_mention = MentionBuilder.chat(chat_id)\n    await bot.answer_message(f"Chat created: {chat_mention}")\n```\n\n### Получение списка пользователей\n*([подробное описание функции](https://ccsteam.atlassian.net/wiki/spaces/SMARTAPP/pages/311001185/Bot+API+BotX+API#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%B0-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B5%D0%B9-%D0%BD%D0%B0-CTS))*\n\n```python\nfrom pybotx import *\n\ncollector = HandlerCollector()\n\n\n@collector.command("/get_users_list", description="Get a list of users")\nasync def users_list_handler(message: IncomingMessage, bot: Bot) -> None:\n    async with bot.users_as_csv(\n        bot_id=message.bot.id,\n        cts_user=True,\n        unregistered=False,\n        botx=False,\n    ) as users:\n        async for user in users:\n            print(user)\n```\n',
    'author': 'Sidnev Nikolay',
    'author_email': 'nsidnev@ccsteam.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ExpressApp/pybotx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
