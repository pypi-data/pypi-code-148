from ..base.processor import Processor


class MockEndpoint(Processor):
  def __init__(self, context, expected_message_count):
    super().__init__()
    self.__exchanges = context.manager.list()
    self.__expected_message_count = expected_message_count

  def process(self, exchange):
    self.exchanges.append(exchange)

  @property
  def exchanges(self):
    return self.__exchanges

  @property
  def expected_message_count(self):
    return self.__expected_message_count