

def defer(func, *args, **kwargs):
   def decorator(mainfunc):
      def subdecorator(*subargs, **subkwargs):
         value = mainfunc(*subargs, **subkwargs)
         func(*args, **kwargs)

         return value
      
      return subdecorator

   return decorator

