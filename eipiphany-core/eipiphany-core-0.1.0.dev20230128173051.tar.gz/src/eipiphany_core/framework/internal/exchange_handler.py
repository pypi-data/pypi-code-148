

class ExchangeHandler(object):
  def __init__(self):
    self.__processor = None
    self.__filter = None
    self.__aggregate = None

  @property
  def processor(self):
    return self.__processor

  @processor.setter
  def processor(self, value):
    self.set_processor(value)

  def set_processor(self, value):
    self.__processor = value
    return self

  @property
  def filter(self):
    return self.__filter

  @filter.setter
  def filter(self, value):
    self.set_filter(value)

  def set_filter(self, value):
    self.__filter = value
    return self

  @property
  def aggregate(self):
    return self.__aggregate

  @aggregate.setter
  def aggregate(self, value):
    self.set_aggregate(value)

  def set_aggregate(self, value):
    self.__aggregate = value
    return self
