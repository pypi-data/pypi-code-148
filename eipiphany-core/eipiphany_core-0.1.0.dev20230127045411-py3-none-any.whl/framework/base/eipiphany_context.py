import time
from multiprocessing import Manager

from .default_eipiphany_context_termination import DefaultEipiphanyContextTermination


class EipiphanyContext(object):
  def __init__(self, termination=DefaultEipiphanyContextTermination()):
    self.__manager = Manager()
    self._routes = []
    self.__processes = []
    self.__start_time = None
    self._termination = termination

  def add_route_builder(self, route_builder):
    route_builder.build()
    for route in route_builder.get_routes():
      self._routes.append(route)
    return self

  def __terminate(self):
    for process in self.__processes:
      process.terminate()
      process.join()
      process.close()

  def start(self):
    self.__start_time = round(time.time() * 1000)
    for route in self._routes:
      for process in route.start():
        self.__processes.append(process)
    terminate = False
    while not terminate:
      time.sleep(1)
      terminate = self._termination.is_terminate(self)
    self.__terminate()

  @property
  def manager(self):
    return self.__manager

  @property
  def processes(self):
    return self.__processes

  @property
  def start_time(self):
    return self.__start_time

  def __enter__(self):
    self.__manager.__enter__()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.__manager.__exit__(exc_type, exc_val, exc_tb)
