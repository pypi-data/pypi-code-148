import hashlib
import secrets
from typing import List, Tuple, Optional
from pbumongo import AbstractMongoStore, AbstractMongoDocument


class User(AbstractMongoDocument):
    """
    Object class representing a document in this database collection.
    """

    def __init__(self):
        super().__init__()
        self.username = None
        self.email = None
        self.user_id = None
        self.password = None
        self.permissions = []
        self.api_key = None
        self.profile = {}

    def to_json(self) -> str:
        """
        Serialises the current instance into JSON
        :return: a dictionary containing the fields and values of this instance
        """
        result = super().to_json()
        if self.username is not None:
            result["username"] = self.username
        if self.permissions is not None:
            result["permissions"] = self.permissions
        if self.email is not None:
            result["email"] = self.email
        if self.user_id is not None:
            result["uid"] = self.user_id
        if self.password is not None:
            result["password"] = self.password
        if self.api_key is not None:
            result["apiKey"] = self.api_key
        if self.profile is not None:
            result["profile"] = self.profile
        return result

    @staticmethod
    def from_json(json: str):
        """
        Method to de-serialise a row from a JSON object
        :param json: the JSON object represented as dictionary
        :return: a representation of a row object
        """
        result = User()
        result.extract_system_fields(json)
        if "username" in json:
            result.username = json["username"]
        if "permissions" in json:
            result.permissions = json["permissions"]
        if "uid" in json:
            result.user_id = json["uid"]
        if "email" in json:
            result.email = json["email"]
        if "password" in json:
            result.password = json["password"]
        if "apiKey" in json:
            result.api_key = json["apiKey"]
        if "profile" in json:
            result.profile = json["profile"]
        return result


class UserStore(AbstractMongoStore):
    """
    Database store representing a MongoDB collection
    """

    def __init__(self, mongo_url: str, mongo_db: str, collection_name: str):
        super().__init__(mongo_url, mongo_db, collection_name, User, 1)

    def get_all(self, page_size=25, page=0) -> Tuple[List[User], int]:
        """
        Returns a list of all users with the given pagination parameters.
        :param page_size: the maximum number of entries to return
        :param page: the page to return (0 is the first page with the first users)
        :return: a tuple containing the list of users and the total number of users in the database
        """
        if page_size is None or page_size == 0:
            # fallback without pagination
            return super().get_all()

        if page is None:
            return self.get_all(page_size, 0)

        # run query
        cursor = self.collection.find({}).skip(page * page_size).limit(page_size)
        # parse user documents
        return list(map(lambda doc: self.object_class.from_json(doc), cursor)), self.collection.count({})

    def create_local_user(self, username: str, password: str, permissions: List[str] = []) -> User:
        if self.get_by_username(username) is not None:
            raise ValueError("Username already in use")
        new_user = User()
        new_user.username = username
        new_user.password = UserStore._md5_password(password)
        new_user.permissions = permissions
        if new_user.permissions is None:
            new_user.permissions = []
        new_id = self.create(new_user.to_json())
        return self.get(new_id)

    def update_permissions(self, user_id, permissions) -> User:
        self.update_one(AbstractMongoStore.id_query(user_id), AbstractMongoStore.set_update("permissions", permissions))
        return self.get(user_id)

    def update_profile(self, user_id, new_profile) -> User:
        self.update_one(AbstractMongoStore.id_query(user_id), AbstractMongoStore.set_update("profile", new_profile))
        return self.get(user_id)

    def change_password(self, user_id, new_password) -> User:
        self.update_one(AbstractMongoStore.id_query(user_id),
                        AbstractMongoStore.set_update("password", UserStore._md5_password(new_password)))
        return self.get(user_id)

    def login_with_password(self, username: str, password: str) -> Optional[User]:
        return self.query_one({
            "username": username,
            "password": UserStore._md5_password(password),
        })

    def get_by_username(self, username: str) -> Optional[User]:
        return self.query_one({
            "username": username,
        })

    def initial_local_user_check(self, initial_username: str, initial_password: str,
                                 initial_permissions=["admin"]) -> Optional[User]:
        if initial_username is None or initial_password is None or len(initial_username) == 0 or len(
                initial_password) == 0:
            raise ValueError("Initial user check failed, because no username or password was provided.")

        number_of_users = self.collection.count()
        if number_of_users == 0:
            # create initial user
            new_user = User()
            new_user.username = initial_username
            new_user.password = UserStore._md5_password(initial_password)
            new_user.permissions = initial_permissions
            new_user_id = self.create(new_user.to_json())
            self.logger.info("Created initial user '{}'".format(initial_username))
            # return newly created user
            return self.get(new_user_id)
        return None

    def create_api_key(self, user_id: str) -> str:
        existing = self.get(user_id)
        if existing is None:
            raise ValueError("No user found for '{}'".format(user_id))
        new_key = secrets.token_hex(16)
        _ = self.update_one(AbstractMongoStore.id_query(user_id), AbstractMongoStore.set_update("apiKey", new_key))
        return new_key

    def revoke_api_key(self, user_id: str):
        existing = self.get(user_id)
        if existing is None:
            raise ValueError("No user found for '{}'".format(user_id))
        _ = self.update_one(AbstractMongoStore.id_query(user_id), AbstractMongoStore.unset_update("apiKey"))

    def get_users_with_api_key(self) -> List[User]:
        return self.query({"apiKey": {"$exists": True}})

    @staticmethod
    def _md5_password(password: str) -> str:
        return hashlib.md5(password.encode("utf-8")).hexdigest()
