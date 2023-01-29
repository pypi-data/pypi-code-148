
class Exchange:

  def __init__(self, body):
    self.__body = body
    self.headers = {}

  def set_header(self, key, value):
    self.headers[key] = value
    return self

  def get_header(self, key):
    return self.headers.get(key)

  @property
  def body(self):
    return self.__body

  @body.setter
  def body(self, value):
    self.set_body(value)

  def set_body(self, body):
    self.__body = body
    return self
