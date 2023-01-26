import abc

class ErrorHandler(metaclass=abc.ABCMeta):

  EXCEPTION_CAUGHT = 'EipyExceptionCaught'

  @abc.abstractmethod
  def handle_exception(self, exchange):
    pass

