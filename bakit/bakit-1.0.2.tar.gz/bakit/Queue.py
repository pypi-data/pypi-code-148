class Queue:
   def __init__(self):
      self.queue = []
   
   def empty(self):
      return len(self.queue) == 0
   
   def get(self):
      try:
         return self.queue.pop(0)
      except:
         return None
      
   def put(self, item):
      self.queue.append(item)
   
   @property
   def unfinished_tasks(self):
      return len(self.queue)