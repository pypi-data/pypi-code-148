from .mock_endpoint import MockEndpoint
from .test_eipiphany_context_termination import TestEipiphanyContextTermination
from ..base.eipiphany_context import EipiphanyContext
from ..internal.exchange_handler import ExchangeHandler


class EipiphanyTestContext(EipiphanyContext):
  def __init__(self, original_context,
      termination=TestEipiphanyContextTermination()):
    self.__original_context = original_context
    self.__mock_endpoints = {}
    self.__original_context._termination = termination
    self.__original_context._termination.mock_endpoints = self.__mock_endpoints

  def add_route_builder(self, route_builder):
    self.__original_context.add_route_builder(route_builder)
    return self

  def start(self):
    self.__original_context.start()

  @property
  def manager(self):
    return self.__original_context.manager

  @property
  def processes(self):
    return self.__original_context.processes

  @property
  def start_time(self):
    return self.__original_context.start_time

  def __enter__(self):
    self.__original_context.__enter__()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.__original_context.__exit__(exc_type, exc_val, exc_tb)

  def __find_route(self, route_id):
    the_route = None
    for route in self.__original_context._routes:
      if route.route_id == route_id:
        the_route = route
    if not the_route:
      raise Exception("Route with id " + route_id + " was not found")
    return the_route

  def mock_endpoint(self, route_id, existing_processor,
      expected_message_count=1):
    the_route = self.__find_route(route_id)
    found = []
    exchange_handlers = the_route._exchange_handlers
    for i in range(len(exchange_handlers)):
      if existing_processor == exchange_handlers[i].processor:
        found.append(i)
    if found:
      offset = 0
      mock_endpoint = MockEndpoint(self.__original_context,
                                   expected_message_count=expected_message_count)
      for i in found:
        exchange_handlers.insert(i + 1 + offset,
                                 ExchangeHandler().set_processor(mock_endpoint))
        offset = offset + 1
      self.__mock_endpoints[existing_processor] = mock_endpoint
    return self

  def mock_endpoint_and_skip(self, route_id, existing_processor,
      expected_message_count=1):
    the_route = self.__find_route(route_id)
    found = []
    exchange_handlers = the_route._exchange_handlers
    for i in range(len(exchange_handlers)):
      if existing_processor == exchange_handlers[i].processor:
        found.append(i)
    if found:
      mock_endpoint = MockEndpoint(self.__original_context,
                                   expected_message_count=expected_message_count)
      for i in found:
        exchange_handlers[i] = ExchangeHandler().set_processor(mock_endpoint)
      self.__mock_endpoints[existing_processor] = mock_endpoint
    return self

  def insert_before_processor(self, route_id, existing_processor, processor):
    the_route = self.__find_route(route_id)
    found = []
    exchange_handlers = the_route._exchange_handlers
    for i in range(len(exchange_handlers)):
      if existing_processor == exchange_handlers[i].processor:
        found.append(i)
    if found:
      offset = 0
      for i in found:
        exchange_handlers.insert(i + offset,
                                 ExchangeHandler().set_processor(processor))
        offset = offset + 1
    return self

  def insert_after_processor(self, route_id, existing_processor, processor):
    the_route = self.__find_route(route_id)
    found = []
    exchange_handlers = the_route._exchange_handlers
    for i in range(len(exchange_handlers)):
      if existing_processor == exchange_handlers[i].processor:
        found.append(i)
    if found:
      offset = 0
      for i in found:
        exchange_handlers.insert(i + 1 + offset,
                                 ExchangeHandler().set_processor(processor))
        offset = offset + 1
    return self

  def replace_processor(self, route_id, existing_processor, processor):
    the_route = self.__find_route(route_id)
    found = []
    exchange_handlers = the_route._exchange_handlers
    for i in range(len(exchange_handlers)):
      if existing_processor == exchange_handlers[i].processor:
        found.append(i)
    if found:
      for i in found:
        exchange_handlers[i] = ExchangeHandler().set_processor(processor)
    return self

  def remove_processor(self, route_id, existing_processor):
    the_route = self.__find_route(route_id)
    found = []
    exchange_handlers = the_route._exchange_handlers
    for i in range(len(exchange_handlers)):
      if existing_processor == exchange_handlers[i].processor:
        found.append(i)
    offset = 0
    if found:
      for i in found:
        exchange_handlers.pop(i + offset)
        offset = offset - 1
    return self

  def replace_from_with(self, route_id, source):
    the_route = self.__find_route(route_id)
    the_route._source_wrapper._source = source
    return self

  @property
  def mock_endpoints(self):
    return self.__mock_endpoints
