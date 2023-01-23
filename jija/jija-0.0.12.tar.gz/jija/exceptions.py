class ViewForceExit(Exception):
    def __init__(self, response):
        self.__response = response

    @property
    def response(self):
        return self.__response
