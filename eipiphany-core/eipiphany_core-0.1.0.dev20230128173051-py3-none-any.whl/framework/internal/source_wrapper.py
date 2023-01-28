class SourceWrapper:

  def __init__(self, source, route):
    self._source = source
    self.__route = route

  def wait_for_events(self):
    while True:
      exchange = self._source.wait_for_event()
      self.__route.process(exchange)

  def start(self):
    return self._source.start()