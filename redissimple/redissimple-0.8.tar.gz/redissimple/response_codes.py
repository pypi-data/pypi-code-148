class ResponseCode():
    # ERROR CODES
    # NOTE :- we are using "-@-" for splitting
    SPLITTER = "-@-"

    GENERIC_ERROR = "1000" + SPLITTER + "Encounter some internal error. Please contact administrator."
    KEY_NOT_FOUND = "1001" + SPLITTER + "File not found."
    CONNECTION_ERROR = "1002" + SPLITTER + "Facing issues in connection to Redis server"

    @staticmethod
    def getResponseMsg(code):
        Code, Message = "", ""
        try:
            if code:
                lst = code.split(ResponseCode.SPLITTER)
                Code, Message = lst[0], lst[1]
            return Code, Message
        except Exception as e:
            return Code, Message
