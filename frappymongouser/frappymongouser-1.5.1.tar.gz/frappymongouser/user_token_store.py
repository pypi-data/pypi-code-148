from datetime import datetime, timedelta
from pbumongo import AbstractMongoDocument, AbstractMongoStore
from pbu import default_options


class UserToken(AbstractMongoDocument):
    def __init__(self, user_id, token, expires, created=datetime.now(), last_update=datetime.now()):
        super().__init__()
        self.user_id = user_id
        self.token = token
        self.expires = expires
        self.created = created
        self.last_update = last_update

    def to_json(self):
        res = {
            "userId": self.user_id,
            "token": self.token,
            "expires": self.expires,
            "created": self.created,
            "lastUpdate": self.last_update,
        }
        return default_options(res, super().to_json())

    @staticmethod
    def from_json(json):
        token = UserToken(json["userId"], json["token"], json["expires"], json["created"], json["lastUpdate"])
        token.extract_system_fields(json)
        return token


class UserTokenStore(AbstractMongoStore):
    """
    MongoDB store that stores user tokens of active login sessions
    """

    def __init__(self, mongo_url, mongo_db, collection_name):
        """
        Creates a new instance of this data store
        """
        super().__init__(mongo_url, mongo_db, collection_name, UserToken, 1)

    def create(self, user_id, token, lifetime=timedelta(days=30)):
        expires = datetime.now() + lifetime
        user_token = UserToken(user_id, token, expires)
        user_token.version = self.data_model_version
        return str(self.collection.insert_one(user_token.to_json()))

    def gey_by_token(self, token):
        return self.query_one({"token": token})

    def clean_up_expired(self):
        self.collection.remove({"expires": {"$lt": datetime.now()}})

    def update_token(self, token_id):
        self.update({"_id": token_id}, {"$set": {"lastUpdate": datetime.now()}})
