# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybotx_smart_logger']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.70.0,<0.75.0', 'pybotx>=0.44.1,<0.55.0']

setup_kwargs = {
    'name': 'pybotx-smart-logger',
    'version': '0.9.8',
    'description': 'Shows logs when you need it',
    'long_description': '# pybotx-smart-logger\n\n_Shows logs when you need it_\n\n\n## Проблема/решение\n\nВ основном наши боты работают в закрытых контурах. Там невозможно использовать Sentry,\nпоэтому наш главный помощник в диагностике неполадок - логи контейнера.\n\nОднако, если сделать логи слишком подробными, то действительно важную информацию будет\nочень сложно найти. Также мы получим проблемы избыточного использования постоянной\nпамяти или слишком быструю ротацию логов. Но сделав логи слишком сжатыми, мы рискуем\nстолкнуться с ситуацией, когда их недостаточно для диагностики ошибки.\n\nТо есть хочется видеть как можно больше информации во время возникновения ошибок, и как\nможно меньше - когда всё хорошо.\n\n\n## Использование\n\nИспользуя функцию `smart_log(log_message: str, *args: Any, **kwargs: Any)` логируете всю\nинформацию, которая поможет в диагностике ошибки. Если во время обработки сообщения\nбудет выброшено исключение, в логи попадёт:\n\n1. Текущее сообщение от пользователя,\n2. Вся залогированная с помощью `smart_log` информация,\n3. Выброшенное исключение.\n\nЕсли обработка сообщения завершится успешно, накопленные логи будут "выброшены".\n\n## Настройка\n\n1. Устанавливаем библиотеку:  \n```bash\npoetry add pybotx-smart-logger\n```\n\n2. Подключим мидлварь для логирования входящих сообщений:\n\n**middlewares/smart_logger.py**\n```python #logger_init_middleware\nasync def smart_logger_middleware(\n    message: IncomingMessage,\n    bot: Bot,\n    call_next: IncomingMessageHandlerFunc,\n) -> None:\n    async with wrap_smart_logger(\n        log_source="Incoming message",\n        context_func=lambda: format_raw_command(message.raw_command),\n        debug=True,\n    ):\n        await call_next(message, bot)\n```\n\n**bot.py**\n```python #logger_init_bot\nBot(\n    collectors=[collector],\n    bot_accounts=[BOT_CREDENTIALS],\n    middlewares=[\n        smart_logger_middleware,\n    ],\n)\n```\n3. Для того чтобы логировать какие-то другие части приложения, необходимо обернуть в контекстный менджер:\n```python #logger_common_use\nasync def handler() -> None:\n    async with wrap_smart_logger(\n        log_source="Request to Server",\n        context_func=lambda: str(kwargs),\n        debug=False,\n    ):\n        await make_request(**kwargs)\n```\n\n4.  Также можно использовать smart_logger для логирования запросов к FastAPI приложению:\n```python #logger_fastapi_use\napp = FastAPI()\n\n\n@app.middleware("http")\nasync def smart_logger_middleware(request: Request, call_next: Callable) -> None:\n    async with wrap_smart_logger(\n        log_source="Incoming request",\n        context_func=lambda: pformat_str_request(request),\n        debug=DEBUG,\n    ):\n        return await call_next(request)\n```\n`log_source` определяет источник логов. `context_func` - пользовательская функция для форматирования логов.\n\n## Пример команд для включения отладки\n\n```python #logger_debug_enable\n@collector.command("/_debug:enable-for-huids", visible=False)\nasync def enable_debug_for_users(message: IncomingMessage, bot: Bot) -> None:\n    try:\n        huids = [UUID(huid) for huid in message.arguments]\n    except ValueError:\n        await bot.answer_message("Получен невалидный user_huid")\n        return\n\n    # TODO: Обновите список user_huid\n\n    await bot.answer_message(f"Список user_huid для отладки обновлён {huids}")\n```\n\n\n```python #logger_debug_enable_command\n@collector.command("/_debug:enable-for-tasks", visible=False)\nasync def enable_debug_for_tasks(message: IncomingMessage, bot: Bot) -> None:\n    # TODO: Обновите список имён задач\n\n    await bot.answer_message("Список задач для отладки обновлён")\n```\n\n\n## Где применять\n\n1. Проверка роли:\n\n```python #logger_check_role\n# TODO: Мидлварь для заполнения message.state.user\n\n\nasync def subscribed_users_only_middleware(\n    message: IncomingMessage,\n    bot: Bot,\n    call_next: IncomingMessageHandlerFunc,\n) -> None:\n    if not message.state.user.is_subscribed:\n        await bot.send(message=only_subscribed_users_allowed_message(message))\n\n        return\n\n    smart_log("This user is subscribed")\n\n    await call_next(message, bot)\n```\n\n2. Обращение в API:\n\n```python #logger_api_call\nasync def _perform_request(\n    method: Literal["GET", "POST"],\n    url: str,\n    query_params: Optional[Dict[str, Any]] = None,\n    body_dict: Optional[Dict[str, Any]] = None,\n) -> str:\n    smart_log("Performing request to YourAwesomeAPI")\n    smart_log("Method:", method)\n    smart_log("URL:", url)\n    smart_log("Query parameters:", query_params)\n    smart_log("Body dict:", body_dict)\n\n    try:\n        async with AsyncClient(base_url=base_url) as client:\n            response = await client.request(\n                method,\n                url,\n                params=query_params,\n                json=body_dict,\n            )\n    except HTTPError as exc:\n        raise RequestToAwesomeAPIError from exc\n\n    smart_log("Response text:", response.text)\n\n    try:\n        response.raise_for_status()\n    except HTTPStatusError as exc:  # noqa: WPS440\n        raise InvalidStatusCodeFromAwesomeAPIError from exc\n\n    return response.text\n```\n\nА также любые моменты, где что-то может пойти не так. Логируйте - не стестяйтесь.\n',
    'author': 'Alexander Samoylenko',
    'author_email': 'alexandr.samojlenko@ccsteam.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
