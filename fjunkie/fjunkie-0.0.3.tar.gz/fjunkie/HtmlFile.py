from fjunkie.File import File

class HtmlFile(File):
	def __init__(self, fname, path):
		self.__ext = ".html"
		
		super().__init__(fname, path, self.__ext)