from concurrent.futures import ThreadPoolExecutor

from .Queue import Queue

class TasksQueue:
   def __init__(self, workers:int=1) -> None:
      self.queue = Queue()
      self.pool = ThreadPoolExecutor(workers)
      
   def execute(self, task, *args, **kwargs):
      unfinished_tasks = self.queue.unfinished_tasks

      self.queue.put({
         "task": task,
         "args": args,
         "kwargs": kwargs
      })

      if unfinished_tasks == 0:
         self.pool.submit(self._execute_all)

   def _execute_all(self):
      while not self.queue.empty():
         task = self.queue.get()
         task["task"](*task["args"], **task["kwargs"])