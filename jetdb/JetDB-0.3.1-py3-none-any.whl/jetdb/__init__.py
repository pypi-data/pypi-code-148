__version__ = '0.3.1'
import time
import os
try:
  import colorama
  global err
except:
  os.system("pip install colorama")

err = colorama.Fore.RED

working = False
class functions:
  #-----------------------------------------#   #--------------REPLACE LINE FUNCTION------------#  
    def index_replace(self, file_name: str, lineindex: str, text: str, msg: bool):
      base = open(file_name, "r")
      ####
      lines = base.read()
      keys = lines.split("\n")
      ####
      for line in keys:
        try:
          global loc
          loc = keys.index(str(lineindex))
        except ValueError:
          pass
        try:
          keys[loc] = str(keys[loc])
          if keys[loc] != text:
            keys[loc] = str(text)
          with open(file_name, "w") as f:
            f.write("\n".join(keys))
            f.close()
        except NameError:
          linename = lineindex
          raise NameError(f'Input Incorrect. No matches: "{linename}" ')
      if msg == True:
        print("Line Replaced")
      elif msg == False:
        pass
      
      
      
    #-----------------------------------------#   #--------------NEW LINE FUNCTION------------#  
          
    def clear(self, name: str, msg: bool):
      w = open(name, "w")
      w.close()
    
    def new_file(self, name: str):
      try:
        x = open(name, "x")
      except FileExistsError:
        print(err+"In line 50 of module JetDB,\nexcept FileExistsError:\n  raise CustomError(error)\n\nFileExistsError: [Errno 17] File exists, data might have been deleted: '{}'".format(name))
        raise SystemExit(err+"> Program died due to incorrect values")
      
      
      

    #-----------------------------------------#   #------------- ADD LINE FUNCTION ------------#
        
    def add(self, file_name: str, text: str, msg: bool):
      f = open(file_name, "a")
      f.write(text+"\n")
      if msg == True:
        print("Line added")
      else:
        pass
    #-----------------------------------------#   #--------------WAIT FUNCTION------------#  
      
    def wait(self, num: int):
      time.sleep(num)
    #-----------------------------------------#   #--------------DELETE LINE FUNCTION------------#  
    def delete_line(self, file_name: str, lineindex: str, linenum: int, string: bool):
      new = []
      if string == True:
        r = open(file_name, "r")
        read = r.read()
        re = read.split("\n")
        for line in read:
          
          try:
            re[loc] = str(re[loc])
            re[loc] = ""
            w = open(file_name, "w")
            w.write("\n".join(re))
            w.close()
          except NameError:
            linename = lineindex
            print(f"Incorrect Input. No matches: {linename}")
            raise SystemExit(err+"> Program died due to incorrect values")

   #-----------------------------------------#   #--------------CHECK LINE/DATA FUNCTION------------# 
    def check_line(self, file_name: str, lineindex: str, linenum: int, string: bool):
      if string == True:
        with open(file_name, "r") as file:
          check = file.read()
        for line in check:
          if line.startswith(lineindex):
            print(line+"\n")
            print("-----------------")
        return
    def printRead(self, filename: str):
      try:
        with open(filename, "r") as f:
          global txt
          txt = f.read()
          f.close()
      except FileNotFoundError:
        print("File does not exist, try again")
      try:
        print(txt)
      except NameError:
        pass

    def index(self, file_name: str, indextext: str):
      global loc
      loc = 0
      global index
      index = ""
      base = open(file_name, "r")
      ####
      lines = base.read()
      keys = lines.split("\n")
      w = open("index.txt", "w")
      w.close()
      ####
      for line in keys:
        loc += 1
        if line.startswith(str(indextext)):
          try:
            index += str(loc)
            index += "\n"
            with open("index.txt", "w") as f:
              f.write(index)
              f.close()
            pass
          except ValueError:
            pass
        else:
          pass  
    def listed_replace(self, file_name: str, listindex: int, text: str, msg: bool):
      base = open(file_name, "r")
      ####
      lines = base.read()
      keys = lines.split("\n")
      ####
      for line in keys:
        try:
          global loc
          loc = listindex
        except ValueError:
          pass
        try:
          keys[loc] = str(keys[loc])
          if keys[loc] != text:
            keys[loc] = str(text)
          with open(file_name, "w") as f:
            f.write("\n".join(keys))
            f.close()
        except NameError:
          linenum = lineindex
          file = file_name
          raise NameError(f'Input Incorrect. Input given was out of range; in {file} "{linenum}" is out of range')
      if msg == True:
        print("Line Replaced")
      elif msg == False:
        pass
    def setup():
      pass