from fjunkie.File import File

class CssFile(File):
	def __init__(self, fname, path):
		self.__ext = ".css"
		
		super().__init__(fname, path, self.__ext)