import os

def exists(path):
	if os.path.exists(path):
		return True
	else:
		return False
		
class File:
	def __init__(self, fname, path, ext):
		self.__fname = fname
		self.__path = path
		self.__ext = ext
		self.__is_printed = False
		
	def path(self):
		return self.__path
		
	def ext(self):
		return self.__ext
		
	def absPath(self):
		return self.__path + self.__fname + self.__ext
		
	def isPrintable(self):
		return self.__is_printed
	
	def isPrinted(self, print_):
		self.__is_printed = print_
		
	def split(self, text, delimiter):
		#text = open(path)
		#text = text.read()
		
		text = text.split(delimiter)
		
		return text
		
	def splits(self, text, delimiters):
		for delimiter in delimiters:
			text = text.replace(delimiter, " ")
			
		text = text.split(" ")
		
		return text
