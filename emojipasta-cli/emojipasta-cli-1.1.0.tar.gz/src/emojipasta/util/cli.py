import argparse

def parse_arguments() -> argparse.Namespace:
  # create the parser
  parser = argparse.ArgumentParser()
  
  # add the arguments
  parser.add_argument("string_to_parse", help="This is the string that will get emojipasta'ed", type=str)
  parser.add_argument("-c", "--commit", help="Option to add the string to a git commit message and commit its", action="store_true")
  # parser.add_argument("-f", "--flag1", help="This is the first flag", action="store_true")
  # parser.add_argument("-a", "--arg", help="This is a new argument", default="default value", type=str)
  
  # parse the arguments
  args = parser.parse_args()
  return args
  
#   # access the flags and argument
#   if args.flag1:
#     # do something if flag1 is set
#   if args.flag2:
#     # do something if flag2 is set
#   print(args.arg)
    
# call the parse_arguments function
