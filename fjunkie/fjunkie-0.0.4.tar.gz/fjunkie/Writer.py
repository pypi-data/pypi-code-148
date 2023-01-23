import os

class Writer:
	def __init__(self, file):
		self.__file = file
		
	def __create(self, msg):
		text = open(self.__file.absPath(), 'w')
		text.write(msg)
		text.close()
		
	def __add(self, msg):
		text = open(self.__file.absPath(), 'a')
		text.write(msg)
		text.close()
		
	def write(self, text):
		if os.path.isdir(self.__file.path()):
			self.__create(text)
		else:
			os.makedirs(self.__file.path())
			self.__create(text)
		
	def append(self, text):
		if os.path.isdir(self.__file.path()):
			self.__add(text)
		else:
			pass
		