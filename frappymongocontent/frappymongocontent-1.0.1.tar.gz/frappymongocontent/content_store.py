from pbumongo import AbstractMongoStore, AbstractMongoDocument


class Content(AbstractMongoDocument):
    def __init__(self):
        super().__init__()
        self.content = None
        self.references = None
        self.content_type = None
        self.label = None

    def to_json(self):
        result = super().to_json()
        if self.content is not None:
            result["content"] = self.content
        if self.references is not None:
            result["references"] = self.references
        if self.content_type is not None:
            result["contentType"] = self.content_type
        if self.label is not None:
            result["label"] = self.label
        return result

    @staticmethod
    def from_json(json):
        content = Content()
        content.extract_system_fields(json)
        if "content" in json:
            content.content = json["content"]
        if "references" in json:
            content.references = json["references"]
        if "contentType" in json:
            content.content_type = json["contentType"]
        if "label" in json:
            content.label = json["label"]
        return content


class ContentStore(AbstractMongoStore):
    def __init__(self, mongo_url, mongo_db, collection_name):
        super().__init__(mongo_url, mongo_db, collection_name, Content, 1)

    def find_by_reference(self, references):
        return super().query({"references": references})

    def find_by_reference_and_content_type(self, references, content_type):
        return super().query({
            "references": references,
            "contentType": content_type,
        })

    def find_by_content_type(self, content_type):
        return super().query({
            "contentType": content_type,
        })

    def update_content(self, content_id, label, references, content):
        return super().update_one(AbstractMongoStore.id_query(content_id),
                                  AbstractMongoStore.set_update(["label", "references", "content"],
                                                                [label, references, content]))
