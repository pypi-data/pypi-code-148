import abc


class EipiphanyContextTermination(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def is_terminate(self, context):
    pass