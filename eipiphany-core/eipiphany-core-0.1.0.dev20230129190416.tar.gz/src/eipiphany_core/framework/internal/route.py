import copy
import logging

from .exchange_handler import ExchangeHandler
from ...framework.base.error_handler import ErrorHandler
from .source_wrapper import SourceWrapper

logger = logging.getLogger(__name__)



class Route(object):

  def __init__(self, source, error_handler, route_id):
    self.__source = source
    self._source_wrapper = SourceWrapper(source, self)
    source.set_source_wrapper(self._source_wrapper)
    self._exchange_handlers = []
    self.__error_handler = error_handler
    self.__route_id = route_id

  @property
  def route_id(self):
    return self.__route_id

  # todo move this to separate class
  def process(self, exchange):
    try:
      next_exchange = copy.deepcopy(exchange)
      for exchange_handler in self._exchange_handlers:
        if exchange_handler.processor:
          exchange_handler.processor.process(next_exchange)
        elif exchange_handler.filter:
          keep_going = exchange_handler.filter.filter(next_exchange)
          if not keep_going:
            break
        elif exchange_handler.aggregate:
          next_exchange = exchange_handler.aggregate.aggregate(next_exchange)
          if not next_exchange:
            break
        else:
          raise Exception("Internal error: invalid exchange handler")
      self.__source.event_success(exchange)
    except Exception as err:
      try:
        exchange.set_header(ErrorHandler.EXCEPTION_CAUGHT, err)
        self.__source.event_failure(err, exchange)
        self.__error_handler.handle_exception(exchange)
      except Exception as err2:
        logger.error("Exception in error handler", exc_info=err2)
        logger.error("Original exception", exc_info=err)

  def to(self, processor):
    self._exchange_handlers.append(ExchangeHandler().set_processor(processor))
    return self

  def filter(self, filter):
    self._exchange_handlers.append(ExchangeHandler().set_filter(filter))
    return self

  def error_handler(self, error_handler):
    self.__error_handler = error_handler
    return self

  def aggregate(self, aggregate):
    self._exchange_handlers.append(ExchangeHandler().set_aggregate(aggregate))
    return self

  def start(self):
    return self._source_wrapper.start()

