from typing import Generic, TYPE_CHECKING, TypeVar

from deci_common.abstractions.base_model import DBSchema
from deci_common.abstractions.abstract_logger import ILogger

if TYPE_CHECKING:
    from typing import Any, Dict, List, Type
    from uuid import UUID

    from deci_common.data_interfaces.mongo_db_interface import MongoDBInterface

T = TypeVar("T", bound=DBSchema)


class DBInterface(Generic[T], ILogger):
    def __init__(self, element_type: "Type[T]", mongo_db_interface: "MongoDBInterface[Dict[str, Any]]"):
        super().__init__()
        self._element_type = element_type
        self._mongo_db_interface = mongo_db_interface

    def insert(self, element: "T") -> "T":
        """
        Insert an element to the DB and return it
        @param element: The element to insert
        @return: T
        """
        self._mongo_db_interface.insert(element.dict())
        return element

    def find(self, search_filter: "Dict[str, Any]" = {}) -> "List[T]":
        """
        Find all elements from DB with a specified search filter
        @param search_filter: Filter for the search
        @return: List[T]
        """
        elements = self._mongo_db_interface.find(search_filter=search_filter)

        return [self._element_type(**element) for element in elements]

    def update(self, element: "T") -> "T":
        """
        Updates an element in the DB using its id
        @param element: The element to update to (id is used to find the element to update)
        @return: T
        """
        self._mongo_db_interface.update(search_filter={"id": element.id}, updated_document=element.dict())
        return element

    def update_many(self, updated_document: "Dict[str, Any]", search_filter: "Dict[str, Any]" = {}) -> "List[T]":
        """
        Updates multiple elements in the DB using the specified search filter
        :param updated_document: the new values to set for the documents
        :param search_filter: documents to update values for
        :return: List[T]
        """
        self._mongo_db_interface.update(search_filter=search_filter, updated_document=updated_document)
        return self.find(search_filter=search_filter)

    def delete(self, _id: "UUID", force: bool = False) -> bool:
        """
        Deletes an element from the DB
        @param _id: The ID of the element to delete
        @param force: if True, permanently delete the element from the DB, otherwise - just mark it as deleted
        @return: True on success, False otherwise
        """
        search_filter = {"id": _id}
        if force:
            delete_result = self._mongo_db_interface.delete(search_filter=search_filter)
            return delete_result.deleted_count == 1
        update_result = self._mongo_db_interface.update(search_filter=search_filter, updated_document={"deleted": True})
        return update_result.modified_count == 1

    def increment_fields(self, *, search_filter: "Dict[str, Any]", fields: "Dict[str, int]") -> bool:
        return self._mongo_db_interface.increment_field(search_filter=search_filter, increment_query=fields)
