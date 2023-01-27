from requests import Session, Response


class WebexTeams(Session):
    """WebexTeams _summary_

    :param token: a valid webex token which can be generated under
        https://developer.webex.com/my-apps/new/integration
        which is described under:
        https://developer.webex.com/docs/getting-your-personal-access-token
    :type token: str
    :param room_id: specify the room id which can be retrieved via the list 
        rooms endpoint which is described under:
        https://developer.webex.com/docs/api/v1/rooms/list-rooms
        You bot has to be member of that room
    :type Session: str
    """

    def __init__(self, token: str, room_id: str = None) -> None:
        super().__init__()
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.room_id = room_id

    def send_message(self, message: str, room_id: str = None) -> Response:
        if not (selected_room_id := (room_id or self.room_id)):
            raise AttributeError("room id is not set")
        
        request_body = {
            "roomId": selected_room_id,
            "markdown": message
        }
        return self.post(
            "https://api.ciscospark.com/v1/messages",
            json = request_body,
        )
