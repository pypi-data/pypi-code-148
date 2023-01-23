from fjunkie.File import File

class PyFile(File):
	def __init__(self, fname, path):
		self.__ext = ".py"
		
		super().__init__(fname, path, self.__ext)