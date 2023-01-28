import time

from ..base.default_eipiphany_context_termination import DefaultEipiphanyContextTermination


class TestEipiphanyContextTermination(DefaultEipiphanyContextTermination):
  def __init__(self, timeout=20000):
    self.__timeout = timeout
    self.__mock_endpoints = {}

  @property
  def mock_endpoints(self):
    return self.__mock_endpoints

  @mock_endpoints.setter
  def mock_endpoints(self, value):
    self.__mock_endpoints = value

  def is_terminate(self, context):
    term = super().is_terminate(context)
    if term:
      return True
    if self.__mock_endpoints.values():
      completed = 0
      for ep in self.__mock_endpoints.values():
        if len(ep.exchanges) >= ep.expected_message_count:
          completed += 1
      if completed == len(self.__mock_endpoints.values()):
        return True
    current_time = round(time.time() * 1000)
    return current_time - context.start_time >= self.__timeout
