class FileSystem:
    def __init__(self, filename):
        self.__filename = filename

    def GetDirectory(self) -> str:
        self.__filename = self.__filename.strip("\\")
        for i in range(-1, -len(self.__filename), -1):
            if self.__filename[i] == "\\":
                return self.__filename[:i] + "\\"
        raise Exception("No directory found")