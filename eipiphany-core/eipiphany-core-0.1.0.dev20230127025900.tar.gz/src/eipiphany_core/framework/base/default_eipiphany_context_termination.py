from .eipiphany_context_termination import EipiphanyContextTermination


class DefaultEipiphanyContextTermination(EipiphanyContextTermination):
  def is_terminate(self, context):
    if not len(context.processes):
      return True
    for process in context.processes:
      if not process.is_alive():
        return True
    return False
