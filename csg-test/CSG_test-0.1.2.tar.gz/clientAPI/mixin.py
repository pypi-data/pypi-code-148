from types import ModuleType
from typing import (Any, Dict, Optional, Type, Union)

import clientAPI.base as base
from .client import CSGList, CSGenome
import clientAPI.utils as exc


__all__ = [
    "GetMixin",
    "GetWithoutIdMixin",
    "RefreshMixin",
    "ListMixin",
    "RetrieveMixin",
    "CreateMixin",
    "UpdateMixin",
    "SetMixin",
    "DeleteMixin",
    "CRUDMixin",
    "NoUpdateMixin",
    "SaveMixin",
    "ObjectDeleteMixin",
    "UserAgentDetailMixin",
    "AccessRequestMixin",
    "DownloadMixin",
    "SubscribableMixin",
    "TodoMixin",
    "TimeTrackingMixin",
    "ParticipantsMixin",
    "BadgeRenderMixin",
]


_RestManagerBase = base.RESTManager
_RestObjectBase = base.RESTObject


class GetMixin(_RestManagerBase):
    # @exc.on_http_error(exc.CSGServerError)
    def get(self, uid=None, params=None):
        """Retrieve a single object.
        Args:
            uid: uid of the object to retrieve
            params: additional query parameters (e.g. filter, column)
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The generated RESTObject.

        Raises:
            // GitlabAuthenticationError: If authentication is not correct
            CSGServerError: If the server cannot perform the request
        """
        try:
            assert (uid != None), "uid cannot be empty"
            assert (isinstance(uid, int)), "uid has to be an integer"
            assert ((not params) or ("filter" not in params.keys())), "filters are not allowed"
            ## easy name stuff here ##
            incoming_filter = params or {}
            # for k,v in kwargs:
            #     if k in self._create_attrs.required:
            #         incoming_filter[k] = v
            server_data = self.csgenome.http_get(path=f'{self._path}/{uid}', params=incoming_filter)
            # print(f'server data: {server_data}')

            try:
                if 'data' in server_data.keys():
                    res = server_data['data']  # TODO: very rigid implementation
                    return self._obj_cls(self, res)
                else:
                    # print(server_data)
                    return server_data['errors']
            except KeyError:
                return server_data
        except AssertionError as e:
            print(f"Input error: {e}")
            return None


class ListMixin(_RestManagerBase):
    _obj_cls: Optional[Type[base.RESTObject]]
    _path: Optional[str]
    csgenome: CSGenome

    def list(self, columns=None, exact=None, order_by=None, desc=False, **kwargs):  # TODO: maybe support none json output in the future
        """Retrieve a list of objects.
        Args:
            all: If True, return all the items, without pagination
            per_page: Number of items to retrieve per request
            page: ID of the page to return (starts with page 1)
            as_list: If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)
        Returns:
            The list of objects, or a generator if `as_list` is False
        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server cannot perform the request
        """
        query_param = self._parse_params(kwargs, columns=columns, exact=exact, order_by=order_by, desc=desc)
        for k, v in query_param.items():
            query_param[k] = v.strip()
        obj, error = self.csgenome.http_list(self._path, query_param)
        if error:
            return obj
        return [self._obj_cls(self, item, created_from_list=True) for item in obj]

    def list_first(self, dictionary=None, columns=None, exact=False, report_count=False, order_by=None, desc=False, **kwargs):
        """
        Return a single object that matches provided properties
        You can pass in a dictionary containing key value pairs to search and filter records by,
        or use keyword parameters as key value pairs instead
        Kwargs:
            exact: True/False (default False)
                If exact, then string fields are case sensitive
            report_count: True/False (default False)
               If true, then returns a tuple (obj, num) where num is the number of 
               records in table that matched the specified search parameters
         **kwargs: values for columns of the table you want to search for (if a dictionary if
         passed in, these kwargs are ignored)
        """
        query_param = self._parse_params(dictionary or kwargs, columns=columns,
                                         exact=exact, order_by=order_by, desc=desc)
        for k, v in query_param.items():
            if isinstance(v, str):
                query_param[k] = v.strip()

        obj, error = self.csgenome.http_list(self._path, query_param)
        # return self._obj_cls(self, obj[0])
        if error or not obj:
            return obj
        if report_count:
            return self._obj_cls(self, obj[0]), len(obj)
        return self._obj_cls(self, obj[0])

    def _parse_params(self, params: Dict, columns: Union[list, str], exact: bool, order_by: str, desc: bool) -> Dict:
        result = {}
        if columns:
            # add column parameter to result, which can either be in form
            # 'column': 'single_col'   OR
            # 'column': ['list', 'of', 'cols']
            result['columns'] = ','.join(columns) if isinstance(columns, list) else str(columns)
        if exact:
            result['filter_mode'] = 'exact'
        for k, v in params.items():
            k = k.replace('__', '.')  # for foreign key fields
            if v is None:
                continue
            if 'filter' in result:  # else we have a combined filter field
                value = ','.join(v) if isinstance(v, list) else v
                result['filter'] += f';{k}:{value}'
            else:  # first filter
                value = ','.join(v) if isinstance(v, list) else v
                result['filter'] = f'{k}:{value}'
        if order_by:
            result['order_by'] = order_by
            if desc:
                result['desc'] = True
        return result

    def gen(self, columns=None, exact=None, order_by=None, desc=False, **kwargs):
        query_param = self._parse_params(kwargs, columns=columns, exact=exact, order_by=order_by, desc=desc)
        for k, v in query_param.items():
            query_param[k] = v.strip()
        if "page" not in query_param.keys():
            query_param['page'] = 1
        if "limit" not in query_param.keys():
            query_param['limit'] = 50
        csg_list = CSGList(self.csgenome, self._path, query_data=query_param)

        return csg_list.gen(lambda item: self._obj_cls(self, item, created_from_list=True))


class CreateMixin(_RestManagerBase):
    _path: Optional[str]
    csgenome: CSGenome

    def _check_missing_create_attrs(self, data):
        missing = []
        for attr in self._create_attrs.required:  # passed in from obj
            if attr not in data:
                missing.append(attr)
        if missing:
            raise AttributeError(f"Missing attributes: {', '.join(missing)}")

    def create(self, data=None, return_response=False):
        """Create a new object.

        Args:
            data: parameters to send to the server to create the
                         resource
            return_response: If true, return the entire response body 
                         dictionary instead of just the data on success 
                         (default False)
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
        Tuple (resp_dict, is_error) containing:
            A dictionary containing server data on success and error
            information on failure 
            and a boolean if error occured or not


        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request
        """
        data = data or {}

        self._check_missing_create_attrs(data)

        path = self._path  # NOTE: might not be necessary, consider

        data = {k: v for k, v in data.items() if v is not None}
        server_data = self.csgenome.http_post(path, post_data=data)

        if 'errors' in server_data:
            # then we have error
            return server_data['errors'], True
        elif 'status' in server_data and not str(server_data['status']).startswith('2'):
            return server_data, True
        elif return_response:
            return server_data, False
        else:
            return server_data['data'], False  # we do not return an object when added


class UpdateMixin(_RestManagerBase):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _obj_cls: Optional[Type[base.RESTObject]]
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    _update_uses_post: bool = False
    csgenome: CSGenome

    def _check_missing_update_attrs(self, data):
        # Remove the id field from the required list as it was previously moved
        # to the http path.
        required = tuple(
            [k for k in self._update_attrs.required if k != self._obj_cls._id_attr]
        )
        missing = []
        for attr in required:
            if attr not in data:
                missing.append(attr)
        if missing:
            raise AttributeError(f"Missing attributes: {', '.join(missing)}")

    def update(self, uid, new_data=None):
        """Update an object on the server.

        Args:
            id: ID of the object to update (can be None if not required)
            new_data: the update data for the object
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The new object data (*not* a RESTObject)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        new_data = new_data or {}

        if uid is None:
            raise AttributeError(f"Missing uid.")
        else:
            path = f"{self._path}/{uid}"

        self._check_missing_update_attrs(new_data)

        server_data = self.csgenome.http_put(path, put_data=new_data)

        if 'data' in server_data.keys():
            res = server_data['data']  # TODO: very rigid implementation
            return self._obj_cls(self, res)
        else:
            return server_data['errors']


# class SetMixin(_RestManagerBase):
#     _computed_path: Optional[str]
#     _from_parent_attrs: Dict[str, Any]
#     _obj_cls: Optional[Type[base.RESTObject]]
#     _parent: Optional[base.RESTObject]
#     _parent_attrs: Dict[str, Any]
#     _path: Optional[str]
#     gitlab: gitlab.Gitlab

#     @exc.on_http_error(exc.GitlabSetError)
#     def set(self, key: str, value: str, **kwargs: Any) -> base.RESTObject:
#         """Create or update the object.

#         Args:
#             key: The key of the object to create/update
#             value: The value to set for the object
#             **kwargs: Extra options to send to the server (e.g. sudo)

#         Raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabSetError: If an error occurred

#         Returns:
#             The created/updated attribute
#         """
#         path = f"{self.path}/{utils.EncodedId(key)}"
#         data = {"value": value}
#         server_data = self.gitlab.http_put(path, post_data=data, **kwargs)
#         if TYPE_CHECKING:
#             assert not isinstance(server_data, requests.Response)
#             assert self._obj_cls is not None
#         return self._obj_cls(self, server_data)


class DeleteMixin(_RestManagerBase):
    _path: Optional[str]
    csgenome: CSGenome

    def delete(self, uid):
        """Delete an object on the server.

        Args:
            id: ID of the object to delete
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        if uid is None:
            raise AttributeError(f"Missing uid.")
        else:
            path = f"{self._path}/{uid}"
        server_data = self.csgenome.http_delete(path)
        return self._obj_cls(self, server_data)


# class CRUDMixin(GetMixin, ListMixin, CreateMixin, UpdateMixin, DeleteMixin):
#     _computed_path: Optional[str]
#     _from_parent_attrs: Dict[str, Any]
#     _obj_cls: Optional[Type[base.RESTObject]]
#     _parent: Optional[base.RESTObject]
#     _parent_attrs: Dict[str, Any]
#     _path: Optional[str]
#     gitlab: gitlab.Gitlab

#     pass


# class NoUpdateMixin(GetMixin, ListMixin, CreateMixin, DeleteMixin):
#     _computed_path: Optional[str]
#     _from_parent_attrs: Dict[str, Any]
#     _obj_cls: Optional[Type[base.RESTObject]]
#     _parent: Optional[base.RESTObject]
#     _parent_attrs: Dict[str, Any]
#     _path: Optional[str]
#     gitlab: gitlab.Gitlab

#     pass


class SaveMixin(_RestObjectBase):
    """Mixin for RESTObject's that can be updated."""

    _id_attr: Optional[str]
    _attrs: Dict[str, Any]
    _module: ModuleType
    _parent_attrs: Dict[str, Any]
    _updated_attrs: Dict[str, Any]
    manager: base.RESTManager

    def _get_updated_data(self):
        updated_data = {}
        for attr in self.manager._update_attrs.required:
            # Get everything required, no matter if it's been updated
            updated_data[attr] = getattr(self, attr)
        # Add the updated attributes
        updated_data.update(self._updated_attrs)

        return updated_data

    def save(self):
        """Save the changes made to the object to the server.

        The object is updated to match what the server returns.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The new object data (*not* a RESTObject)

        Raise:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        updated_data = self._get_updated_data()
        # Nothing to update. Server fails if sent an empty dict.
        if not updated_data:
            return None

        # call the manager
        obj_id = self.encoded_id
        server_data = self.manager.update(uid=obj_id, new_data=updated_data)
        self._update_attrs(server_data)
        return server_data


class ObjectDeleteMixin(_RestObjectBase):
    """Mixin for RESTObject's that can be deleted."""

    _id_attr: Optional[str]
    _attrs: Dict[str, Any]
    _module: ModuleType
    _parent_attrs: Dict[str, Any]
    _updated_attrs: Dict[str, Any]
    manager: base.RESTManager

    def delete(self, **kwargs: Any) -> None:
        """Delete the object from the server.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        self.manager.delete(self.encoded_id, **kwargs)


# class UserAgentDetailMixin(_RestObjectBase):
#     _id_attr: Optional[str]
#     _attrs: Dict[str, Any]
#     _module: ModuleType
#     _parent_attrs: Dict[str, Any]
#     _updated_attrs: Dict[str, Any]
#     manager: base.RESTManager

#     @cli.register_custom_action(("Snippet", "ProjectSnippet", "ProjectIssue"))
#     @exc.on_http_error(exc.GitlabGetError)
#     def user_agent_detail(self, **kwargs: Any) -> Dict[str, Any]:
#         """Get the user agent detail.

#         Args:
#             **kwargs: Extra options to send to the server (e.g. sudo)

#         Raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabGetError: If the server cannot perform the request
#         """
#         path = f"{self.manager.path}/{self.encoded_id}/user_agent_detail"
#         result = self.manager.gitlab.http_get(path, **kwargs)
#         if TYPE_CHECKING:
#             assert not isinstance(result, requests.Response)
#         return result


# class AccessRequestMixin(_RestObjectBase):
#     _id_attr: Optional[str]
#     _attrs: Dict[str, Any]
#     _module: ModuleType
#     _parent_attrs: Dict[str, Any]
#     _updated_attrs: Dict[str, Any]
#     manager: base.RESTManager

#     @cli.register_custom_action(
#         ("ProjectAccessRequest", "GroupAccessRequest"), tuple(), ("access_level",)
#     )
#     @exc.on_http_error(exc.GitlabUpdateError)
#     def approve(
#         self, access_level: int = gitlab.const.DEVELOPER_ACCESS, **kwargs: Any
#     ) -> None:
#         """Approve an access request.

#         Args:
#             access_level: The access level for the user
#             **kwargs: Extra options to send to the server (e.g. sudo)

#         Raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabUpdateError: If the server fails to perform the request
#         """

#         path = f"{self.manager.path}/{self.encoded_id}/approve"
#         data = {"access_level": access_level}
#         server_data = self.manager.gitlab.http_put(path, post_data=data, **kwargs)
#         if TYPE_CHECKING:
#             assert not isinstance(server_data, requests.Response)
#         self._update_attrs(server_data)


# class DownloadMixin(_RestObjectBase):
#     _id_attr: Optional[str]
#     _attrs: Dict[str, Any]
#     _module: ModuleType
#     _parent_attrs: Dict[str, Any]
#     _updated_attrs: Dict[str, Any]
#     manager: base.RESTManager

#     @cli.register_custom_action(("GroupExport", "ProjectExport"))
#     @exc.on_http_error(exc.GitlabGetError)
#     def download(
#         self,
#         streamed: bool = False,
#         action: Optional[Callable] = None,
#         chunk_size: int = 1024,
#         **kwargs: Any,
#     ) -> Optional[bytes]:
#         """Download the archive of a resource export.

#         Args:
#             streamed: If True the data will be processed by chunks of
#                 `chunk_size` and each chunk is passed to `action` for
#                 treatment
#             action: Callable responsible of dealing with chunk of
#                 data
#             chunk_size: Size of each chunk
#             **kwargs: Extra options to send to the server (e.g. sudo)

#         Raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabGetError: If the server failed to perform the request

#         Returns:
#             The blob content if streamed is False, None otherwise
#         """
#         path = f"{self.manager.path}/download"
#         result = self.manager.gitlab.http_get(
#             path, streamed=streamed, raw=True, **kwargs
#         )
#         if TYPE_CHECKING:
#             assert isinstance(result, requests.Response)
#         return utils.response_content(result, streamed, action, chunk_size)


# class SubscribableMixin(_RestObjectBase):
#     _id_attr: Optional[str]
#     _attrs: Dict[str, Any]
#     _module: ModuleType
#     _parent_attrs: Dict[str, Any]
#     _updated_attrs: Dict[str, Any]
#     manager: base.RESTManager

#     @cli.register_custom_action(
#         ("ProjectIssue", "ProjectMergeRequest", "ProjectLabel", "GroupLabel")
#     )
#     @exc.on_http_error(exc.GitlabSubscribeError)
#     def subscribe(self, **kwargs: Any) -> None:
#         """Subscribe to the object notifications.

#         Args:
#             **kwargs: Extra options to send to the server (e.g. sudo)

#         raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabSubscribeError: If the subscription cannot be done
#         """
#         path = f"{self.manager.path}/{self.encoded_id}/subscribe"
#         server_data = self.manager.gitlab.http_post(path, **kwargs)
#         if TYPE_CHECKING:
#             assert not isinstance(server_data, requests.Response)
#         self._update_attrs(server_data)

#     @cli.register_custom_action(
#         ("ProjectIssue", "ProjectMergeRequest", "ProjectLabel", "GroupLabel")
#     )
#     @exc.on_http_error(exc.GitlabUnsubscribeError)
#     def unsubscribe(self, **kwargs: Any) -> None:
#         """Unsubscribe from the object notifications.

#         Args:
#             **kwargs: Extra options to send to the server (e.g. sudo)

#         raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabUnsubscribeError: If the unsubscription cannot be done
#         """
#         path = f"{self.manager.path}/{self.encoded_id}/unsubscribe"
#         server_data = self.manager.gitlab.http_post(path, **kwargs)
#         if TYPE_CHECKING:
#             assert not isinstance(server_data, requests.Response)
#         self._update_attrs(server_data)


# class TodoMixin(_RestObjectBase):
#     _id_attr: Optional[str]
#     _attrs: Dict[str, Any]
#     _module: ModuleType
#     _parent_attrs: Dict[str, Any]
#     _updated_attrs: Dict[str, Any]
#     manager: base.RESTManager

#     @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"))
#     @exc.on_http_error(exc.GitlabTodoError)
#     def todo(self, **kwargs: Any) -> None:
#         """Create a todo associated to the object.

#         Args:
#             **kwargs: Extra options to send to the server (e.g. sudo)

#         Raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabTodoError: If the todo cannot be set
#         """
#         path = f"{self.manager.path}/{self.encoded_id}/todo"
#         self.manager.gitlab.http_post(path, **kwargs)


# class TimeTrackingMixin(_RestObjectBase):
#     _id_attr: Optional[str]
#     _attrs: Dict[str, Any]
#     _module: ModuleType
#     _parent_attrs: Dict[str, Any]
#     _updated_attrs: Dict[str, Any]
#     manager: base.RESTManager

#     @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"))
#     @exc.on_http_error(exc.GitlabTimeTrackingError)
#     def time_stats(self, **kwargs: Any) -> Dict[str, Any]:
#         """Get time stats for the object.

#         Args:
#             **kwargs: Extra options to send to the server (e.g. sudo)

#         Raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabTimeTrackingError: If the time tracking update cannot be done
#         """
#         # Use the existing time_stats attribute if it exist, otherwise make an
#         # API call
#         if "time_stats" in self.attributes:
#             return self.attributes["time_stats"]

#         path = f"{self.manager.path}/{self.encoded_id}/time_stats"
#         result = self.manager.gitlab.http_get(path, **kwargs)
#         if TYPE_CHECKING:
#             assert not isinstance(result, requests.Response)
#         return result

#     @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"), ("duration",))
#     @exc.on_http_error(exc.GitlabTimeTrackingError)
#     def time_estimate(self, duration: str, **kwargs: Any) -> Dict[str, Any]:
#         """Set an estimated time of work for the object.

#         Args:
#             duration: Duration in human format (e.g. 3h30)
#             **kwargs: Extra options to send to the server (e.g. sudo)

#         Raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabTimeTrackingError: If the time tracking update cannot be done
#         """
#         path = f"{self.manager.path}/{self.encoded_id}/time_estimate"
#         data = {"duration": duration}
#         result = self.manager.gitlab.http_post(path, post_data=data, **kwargs)
#         if TYPE_CHECKING:
#             assert not isinstance(result, requests.Response)
#         return result

#     @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"))
#     @exc.on_http_error(exc.GitlabTimeTrackingError)
#     def reset_time_estimate(self, **kwargs: Any) -> Dict[str, Any]:
#         """Resets estimated time for the object to 0 seconds.

#         Args:
#             **kwargs: Extra options to send to the server (e.g. sudo)

#         Raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabTimeTrackingError: If the time tracking update cannot be done
#         """
#         path = f"{self.manager.path}/{self.encoded_id}/reset_time_estimate"
#         result = self.manager.gitlab.http_post(path, **kwargs)
#         if TYPE_CHECKING:
#             assert not isinstance(result, requests.Response)
#         return result

#     @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"), ("duration",))
#     @exc.on_http_error(exc.GitlabTimeTrackingError)
#     def add_spent_time(self, duration: str, **kwargs: Any) -> Dict[str, Any]:
#         """Add time spent working on the object.

#         Args:
#             duration: Duration in human format (e.g. 3h30)
#             **kwargs: Extra options to send to the server (e.g. sudo)

#         Raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabTimeTrackingError: If the time tracking update cannot be done
#         """
#         path = f"{self.manager.path}/{self.encoded_id}/add_spent_time"
#         data = {"duration": duration}
#         result = self.manager.gitlab.http_post(path, post_data=data, **kwargs)
#         if TYPE_CHECKING:
#             assert not isinstance(result, requests.Response)
#         return result

#     @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"))
#     @exc.on_http_error(exc.GitlabTimeTrackingError)
#     def reset_spent_time(self, **kwargs: Any) -> Dict[str, Any]:
#         """Resets the time spent working on the object.

#         Args:
#             **kwargs: Extra options to send to the server (e.g. sudo)

#         Raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabTimeTrackingError: If the time tracking update cannot be done
#         """
#         path = f"{self.manager.path}/{self.encoded_id}/reset_spent_time"
#         result = self.manager.gitlab.http_post(path, **kwargs)
#         if TYPE_CHECKING:
#             assert not isinstance(result, requests.Response)
#         return result


# class ParticipantsMixin(_RestObjectBase):
#     _id_attr: Optional[str]
#     _attrs: Dict[str, Any]
#     _module: ModuleType
#     _parent_attrs: Dict[str, Any]
#     _updated_attrs: Dict[str, Any]
#     manager: base.RESTManager

#     @cli.register_custom_action(("ProjectMergeRequest", "ProjectIssue"))
#     @exc.on_http_error(exc.GitlabListError)
#     def participants(self, **kwargs: Any) -> Dict[str, Any]:
#         """List the participants.

#         Args:
#             all: If True, return all the items, without pagination
#             per_page: Number of items to retrieve per request
#             page: ID of the page to return (starts with page 1)
#             as_list: If set to False and no pagination option is
#                 defined, return a generator instead of a list
#             **kwargs: Extra options to send to the server (e.g. sudo)

#         Raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabListError: If the list could not be retrieved

#         Returns:
#             The list of participants
#         """

#         path = f"{self.manager.path}/{self.encoded_id}/participants"
#         result = self.manager.gitlab.http_get(path, **kwargs)
#         if TYPE_CHECKING:
#             assert not isinstance(result, requests.Response)
#         return result


# class BadgeRenderMixin(_RestManagerBase):
#     @cli.register_custom_action(
#         ("GroupBadgeManager", "ProjectBadgeManager"), ("link_url", "image_url")
#     )
#     @exc.on_http_error(exc.GitlabRenderError)
#     def render(self, link_url: str, image_url: str, **kwargs: Any) -> Dict[str, Any]:
#         """Preview link_url and image_url after interpolation.

#         Args:
#             link_url: URL of the badge link
#             image_url: URL of the badge image
#             **kwargs: Extra options to send to the server (e.g. sudo)

#         Raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabRenderError: If the rendering failed

#         Returns:
#             The rendering properties
#         """
#         path = f"{self.path}/render"
#         data = {"link_url": link_url, "image_url": image_url}
#         result = self.gitlab.http_get(path, data, **kwargs)
#         if TYPE_CHECKING:
#             assert not isinstance(result, requests.Response)
#         return result


# class PromoteMixin(_RestObjectBase):
#     _id_attr: Optional[str]
#     _attrs: Dict[str, Any]
#     _module: ModuleType
#     _parent_attrs: Dict[str, Any]
#     _updated_attrs: Dict[str, Any]
#     _update_uses_post: bool = False
#     manager: base.RESTManager

#     def _get_update_method(
#         self,
#     ) -> Callable[..., Union[Dict[str, Any], requests.Response]]:
#         """Return the HTTP method to use.

#         Returns:
#             http_put (default) or http_post
#         """
#         if self._update_uses_post:
#             http_method = self.manager.gitlab.http_post
#         else:
#             http_method = self.manager.gitlab.http_put
#         return http_method

#     @exc.on_http_error(exc.GitlabPromoteError)
#     def promote(self, **kwargs: Any) -> Dict[str, Any]:
#         """Promote the item.

#         Args:
#             **kwargs: Extra options to send to the server (e.g. sudo)

#         Raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabPromoteError: If the item could not be promoted
#             GitlabParsingError: If the json data could not be parsed

#         Returns:
#             The updated object data (*not* a RESTObject)
#         """

#         path = f"{self.manager.path}/{self.encoded_id}/promote"
#         http_method = self._get_update_method()
#         result = http_method(path, **kwargs)
#         if TYPE_CHECKING:
#             assert not isinstance(result, requests.Response)
#         return result
