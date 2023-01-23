import os

def exists(path):
	if os.path.exists(path):
		return True
	else:
		return False

class Reader:
	def __init__(self, file):
		self.__file = file
		
	def file(self):
		return self.__file
		
	def text(self):
		if exists(self.__file.path()):
			text = open(self.__file.path(), 'r')
			info = text.read()
			text.close()
		
			if self.__file.isPrintable():
				print(info)
			
			return text
		else:
			print("Invalid File")
			
	def chars(self):
		if exists(self.__file.path()):
			text = open(self.__file.path(), 'r')
			info = text.read()
			text.close()
			
			chars = []
			for char in info:
				chars.append(char)
				if self.__file.isPrintable():
					print(char)
			return chars
		else:
			print("Invalid File")
		
	def words(self):
		if exists(self.__file.path()):
			text = open(self.__file.path(), 'r')
			info = text.read()
			text.close()
			
			delimits = [" ", ",", "/"]
			words = self.__file.splits(info, delimits)
		
			if self.__file.isPrintable():
				for word in words:
					print(word)
			
			return words
		else:
			print("Invalid File")