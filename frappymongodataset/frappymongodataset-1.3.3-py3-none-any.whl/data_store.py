from pandas import DataFrame
from frappymongodataset.mmacommon import imagefile_to_ndarray
from pbumongo import AbstractMongoStore, AbstractMongoDocument


class DataTypes:
    TIME_SERIES = "TIME_SERIES"
    IMAGE = "IMAGE"
    JSON = "JSON"
    BINARY = "BINARY"


ALL_TYPES = [DataTypes.TIME_SERIES, DataTypes.IMAGE, DataTypes.JSON, DataTypes.BINARY]


class DataJsonPayload:
    def __init__(self):
        self.data = {}

    def to_json(self):
        return self.data

    @staticmethod
    def from_json(json):
        data = DataJsonPayload()
        data.data = json
        return data


class DataTimeSeriesPayload:
    def __init__(self):
        self.column_mapping = {}
        self.columns = []
        self.index_column = None
        self.data = []
        self.date_format = None

    def to_json(self):
        result = {
            "columnMapping": self.column_mapping,
            "columns": self.columns,
            "data": self.data,
        }
        if self.index_column is not None:
            result["indexColumn"] = self.index_column
        if self.date_format is not None:
            result["dateFormat"] = self.date_format
        return result

    def to_pd_data_frame(self):
        input_data = {}
        for col_index, col_name in enumerate(self.columns):
            input_data[col_name] = [x[col_index] for x in self.data]
        return DataFrame(input_data).set_index(self.index_column)

    @staticmethod
    def from_json(json):
        result = DataTimeSeriesPayload()
        if "columnMapping" in json:
            result.column_mapping = json["columnMapping"]
        if "columns" in json:
            result.columns = json["columns"]
        if "data" in json:
            result.data = json["data"]
        if "indexColumn" in json:
            result.index_column = json["indexColumn"]
        if "dateFormat" in json:
            result.date_format = json["dateFormat"]
        return result


class DataBinaryPayload:
    def __init__(self):
        self.target_file = None
        self.mime_type = None
        self.public_flag = False

    def to_json(self):
        result = {}
        if self.target_file is not None:
            result["targetFile"] = self.target_file
        if self.mime_type is not None:
            result["mimeType"] = self.mime_type
        if self.public_flag is not None:
            result["publicFlag"] = self.public_flag
        return result

    def extract_base_fields(self, json):
        if "targetFile" in json:
            self.target_file = json["targetFile"]
        if "mimeType" in json:
            self.mime_type = json["mimeType"]
        if "publicFlag" in json:
            self.public_flag = json["publicFlag"]

    @staticmethod
    def from_json(json):
        result = DataBinaryPayload()
        result.extract_base_fields(json)
        return result


class DataImagePayload(DataBinaryPayload):
    def __init__(self):
        super().__init__()
        self.dimensions = {}
        self.thumbnail = None

    def to_json(self):
        result = super().to_json()
        result["dimensions"] = self.dimensions
        if self.thumbnail is not None:
            result["thumbnail"] = self.thumbnail
        return result

    def to_np_array(self):
        return imagefile_to_ndarray(self.target_file)

    @staticmethod
    def from_json(json):
        result = DataImagePayload()
        result.extract_base_fields(json)
        if "dimensions" in json:
            result.dimensions = json["dimensions"]
        if "thumbnail" in json:
            result.thumbnail = json["thumbnail"]
        return result


class Data(AbstractMongoDocument):

    def __init__(self):
        super().__init__()
        self.type = None
        self.label = None
        self.payload = None
        self.user_id = None
        self.assignments = []
        self.relations = []

    def to_json(self):
        result = super().to_json()
        if self.type is not None:
            result["type"] = self.type
        if self.payload is not None:
            result["payload"] = self.payload.to_json()
        if self.label is not None:
            result["label"] = self.label
        if self.user_id is not None:
            result["userId"] = self.user_id
        if self.assignments is not None:
            result["assignments"] = self.assignments
        if self.relations is not None:
            result["relations"] = self.relations
        return result

    def to_pd_data_frame(self):
        if self.type != DataTypes.TIME_SERIES:
            raise ValueError("Data set is not a TIME_SERIES")
        if self.payload is None:
            raise ValueError("Data set doesn't have a payload")
        return self.payload.to_pd_data_frame()

    def to_np_array(self):
        if self.type != DataTypes.IMAGE:
            raise ValueError("Data set is not a TIME_SERIES")
        if self.payload is None:
            raise ValueError("Data set doesn't have a payload")
        return self.payload.to_np_array()

    @staticmethod
    def from_json(json):
        data = Data()
        data.extract_system_fields(json)
        if "type" in json:
            data.type = json["type"]
            if "payload" in json:
                if data.type == DataTypes.TIME_SERIES:
                    data.payload = DataTimeSeriesPayload.from_json(json["payload"])
                elif data.type == DataTypes.IMAGE:
                    data.payload = DataImagePayload.from_json(json["payload"])
                elif data.type == DataTypes.JSON:
                    data.payload = DataJsonPayload.from_json(json["payload"])
                elif data.type == DataTypes.BINARY:
                    data.payload = DataBinaryPayload.from_json(json["payload"])
        if "label" in json:
            data.label = json["label"]
        if "userId" in json:
            data.user_id = json["userId"]
        if "assignments" in json:
            data.assignments = json["assignments"]
        if "relations" in json:
            data.relations = json["relations"]
        return data


class DataStore(AbstractMongoStore):
    def __init__(self, mongo_url, mongo_db, collection_name):
        super().__init__(mongo_url, mongo_db, collection_name, Data, 1)

    def get_all(self):
        return list(map(lambda x: Data.from_json(x), self.collection.find({}, {"payload": 0})))

    def get_meta(self, data_id):
        result = self.collection.find_one(AbstractMongoStore.id_query(data_id), {"payload": 0})
        if result is None:
            return None
        return Data.from_json(result)

    def update_meta(self, data_id, meta_update):
        if "relations" not in meta_update:
            meta_update["relations"] = []
        update_keys = ["label", "assignments", "relations"]
        update_values = [meta_update["label"], meta_update["assignments"], meta_update["relations"]]
        if "payload" in meta_update:
            for payload_key in meta_update["payload"]:
                update_keys.append("payload.{}".format(payload_key))
                update_values.append(meta_update["payload"][payload_key])

        update = AbstractMongoStore.set_update(update_keys, update_values)
        return self.collection.update_one(AbstractMongoStore.id_query(data_id), update)

    def get_by_type(self, data_type):
        res = self.collection.find({"type": data_type}, {"payload": 0})
        return list(map(lambda x: Data.from_json(x), res))

    def get_by_assignment_and_type(self, assignment_id, data_type):
        res = self.collection.find(
            {
                "assignments.{}".format(assignment_id): {"$exists": True},
                "type": data_type,
            }, {"payload": 0})
        return list(map(lambda x: Data.from_json(x), res))

    def get_by_assignment(self, assignment_id):
        res = self.collection.find({"assignments.{}".format(assignment_id): {"$exists": True}}, {"payload": 0})
        return list(map(lambda x: Data.from_json(x), res))

    def get_by_assignment_type(self, assignment_id, assignment_type):
        res = self.collection.find({
            "assignments.{}".format(assignment_id): assignment_type,
        }, {"payload": 0})
        return list(map(lambda x: Data.from_json(x), res))

    def get_by_relations(self, data_set_id):
        res = self.collection.find({
            "relations": data_set_id,
        }, {"payload": 0})
        return list(map(lambda x: Data.from_json(x), res))

    def update_target_file(self, doc_id, target_path):
        return self.update_one(AbstractMongoStore.id_query(doc_id),
                               AbstractMongoStore.set_update("payload.targetFile", target_path))

    # overwrite the 2 delete methods to avoid issues with relations

    def delete(self, doc_id):
        self.update({"relations": doc_id}, {"$pull": {"relations": doc_id}})
        return super().delete(doc_id)

    def delete_many(self, query):
        for doc in self.collection.find(query, {"_id": 1}):
            doc_id = str(doc["_id"])
            self.delete(doc_id)
