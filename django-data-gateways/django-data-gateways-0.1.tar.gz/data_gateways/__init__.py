from .services.core import registry
from .services.sending import senders
from .services.sending import strategies


# Регистрация встроенных отправщиков и стратегий.
sender_registry = registry.SenderRegistry()
sender_registry.register(senders.EmailSender)
sender_registry.register(senders.TelegramSender)


# Регистрация встроенных стратегий отправки.
strategy_registry = registry.StrategyRegistry()
strategy_registry.register(strategies.AllSystemsSendStrategy)
strategy_registry.register(strategies.FirstSuccessSystemSendStrategy)
