import base64
from ecmind_blue_client_manage.system_role import SystemRole
from .access import Access
from typing import List
from ecmind_blue_client import Client, Job, Jobs, Param, ParamTypes
from XmlElement import XmlElement
import time
from ftfy import fix_encoding


def get_users(client: Client) -> dict:
    user_list_result = client.execute(Job("mng.GetUserList", Flags=0))

    if not user_list_result.return_code == 0:
        raise RuntimeError(user_list_result.error_message)

    xml_string = fix_encoding(user_list_result.values["UserList"])
    users_element = XmlElement.from_string(xml_string).find("Users")
    users_element.find("User").flag_as_list = True
    result = {}
    for user_entry in users_element.to_dict()["User"]:
        result[user_entry["@benutzer"]] = {
            "id": user_entry["@id"],
            "login": user_entry["@benutzer"],
            "name": user_entry["@name"],
            "guid": user_entry["@osguid"],
            "mail": user_entry["@osemail"],
            "locked": True if user_entry["@locked"] == 1 else False,
            "profile": user_entry["@profil"],
        }
    return result


def get_user_ids(client: Client) -> dict:
    return {u["id"]: u for u in get_users(client).values()}


def get_user_guids(client: Client) -> dict:
    return {u["guid"]: u for u in get_users(client).values()}


def get_sessions(client: Client) -> list[dict[str, str]]:
    job = Job("krn.SessionEnumDB", Flags=0)

    result_get_sessions = client.execute(job)
    if not result_get_sessions.return_code == 0:
        raise RuntimeError(result_get_sessions.error_message)

    sessions = []

    for session_data_encoded in result_get_sessions.values["Sessions"].split(";"):
        if len(session_data_encoded) == 0:
            break

        session_data = (
            base64.b64decode(session_data_encoded.encode("utf-8"))
            .decode("utf-8")
            .split("\x00")
        )
        session = {
            info: session_data[i]
            for i, info in enumerate(
                result_get_sessions.values["SessionInfoType"].split(";")
            )
        }

        sessions.append(session)

    return sessions


def get_system_roles(client: Client, login: str) -> List[SystemRole]:
    job = Job("mng.GetUserRoles")
    job.append(Param("Flags", ParamTypes.INTEGER, 0))
    job.append(Param("$$$SwitchContextUserName$$$", ParamTypes.STRING, login))
    result_user_roles = client.execute(job)

    if result_user_roles.return_code != 0:
        raise RuntimeError(result_user_roles.error_message)

    return [
        SystemRole(int(r))
        for r in str(result_user_roles.values["Result"]).strip(";").split(";")
        if len(r)
    ]


def get_user_groups_by_guid(client: Client, guid: str) -> List[str]:
    job = Job("mng.GetUserGroups", Flags=0, OutputUnicode=1, UserGUID=guid)
    get_user_groups_result = client.execute(job)
    if get_user_groups_result.return_code != 0:
        raise RuntimeError(get_user_groups_result.error_message)

    if "utfGroupList" in get_user_groups_result.values:
        groups = XmlElement.from_string(get_user_groups_result.values["utfGroupList"])[
            "Groups"
        ][0]
    else:
        groups = XmlElement.from_string(get_user_groups_result.values["GroupList"])[
            "Groups"
        ][0]

    first_group = groups.find("Group")
    if first_group == None:
        raise RuntimeError("No groups found.")
    first_group.flag_as_list = True

    result = {}
    for group_entry in groups.to_dict(recognize_bool=False)["Group"]:
        result[group_entry["@name"]] = {
            "id": group_entry["@id"],
            "name": group_entry["@name"],
            "description": group_entry["@description"],
            "guid": group_entry["@osguid"],
            "profil": True if group_entry["@profil"] == 1 else False,
        }
    return result


def get_user_groups_by_login(client: Client, login: str) -> List[str]:
    """This is a relatively inefficient comfort function using get_users() beforehand get_user_group_by_guid()."""
    users = get_users(client)
    guid = users[login]["guid"]
    return get_user_groups_by_guid(client, guid)


def check_permissions(
    client: Client,
    objects: dict[int, list[int]],
    access: Access = None,
    context_user: str = None,
    special_cases: bool = False,
    folder_id: int = None,
    register_id: int = None,
    register_type_id: int = None,
) -> dict[int, Access]:
    """
    Check the access permissions for DMS objects.

    Keyword arguments:
        - client: A ecmind_blue_client instance.
        - objects: A dictionary of object type ids and lists of corresponding object ids to check permissions.
        - (Optional) access: The access types to check for packed as an Access object.
        - (Optional) context_user: Username to check access rights for. Uses current login when omitted.
        - (Optional) special_cases: Boolean to indicate if filing tray objects, inactive variants and shared
            objects should be processed. Activating this leads to a separate API call for each object id.
        - (Optional) folder_id: The id of a target folder for move operations.
        - (Optional) register_id: The id of a target register for move operations.
        - (Optional) register_type_id: The type id of a target register for move operations. Two magic values
            exist: `0`: The object is in no register, `-1`: The register context is not checked.

    Returns a dict of object ids and their effective access objects.
    """

    context = {}
    if folder_id != None:
        context["FolderID"] = folder_id
    if register_id != None:
        context["RegisterID"] = register_id
    if register_type_id != None:
        context["RegisterType"] = register_type_id

    if special_cases:
        job = Job(
            jobname=Jobs.DMS_CHECKPERMISSION,
            context_user=context_user,
            Flags=0,
            Access=str(access) if access else str(Access(True, True, True, True, True)),
            **context,
        )

        result = {}
        for type_id, object_ids in objects.items():
            job.update(Param("ObjectType", ParamTypes.INTEGER, type_id))
            for object_id in object_ids:
                job.update(Param("ObjectID", ParamTypes.INTEGER, object_id))
                job_result = client.execute(job)

                if job_result.return_code != 0:
                    raise RuntimeError(job_result.error_message)

                result[object_id] = Access.from_string(job_result.values["Access"])

        return result

    else:
        job = Job(
            jobname=Jobs.DMS_CHECKPERMISSIONS,
            context_user=context_user,
            Flags=0,
            Access=str(access) if access else str(Access(True, True, True, True, True)),
            **{f"ObjectType{tid[0]}": tid[1] for tid in enumerate(objects.keys(), 1)},
            **{
                f"ObjectList{oid[0]}": ",".join(map(str, oid[1]))
                for oid in enumerate(objects.values(), 1)
            },
            **context,
        )

        job_result = client.execute(job)

        if job_result.return_code != 0:
            raise RuntimeError(job_result.error_message)

        result = {}
        i = 1
        while f"ObjectType{i}" in job_result.values:
            result.update(
                {
                    int(x[0]): Access.from_string(x[1])
                    for x in [
                        oid_and_access.split(":")
                        for oid_and_access in job_result.values[f"ObjectList{i}"].split(
                            ","
                        )
                    ]
                }
            )
            i += 1

        return result


def check_doccollaboration(
    client: Client, objects: dict[int, list[int]], context_user: str = None
) -> dict[int, Access]:
    """
    Check the access permissions for DMS objects.

    Keyword arguments:
        - client: A ecmind_blue_client instance.
        - objects: A dictionary of object type ids and lists of corresponding object ids to check permissions.
        - (Optional) context_user: Username to check access rights for. Uses current login when omitted.

    Returns a dict of object ids and their effective access objects.
    """

    # Es dürfen nur Dokumente übergeben werden
    result = {}

    current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    for type_id, object_ids in objects.items():
        if type_id <= 999 or str(type_id)[0:2] == "64":
            # ist Register oder Folder
            return None
        else:
            if context_user is None:
                context_user = client.username

            for obj in object_ids:

                sql_statement = f"""
                                    SELECT
                                    *
                                    FROM
                                    osdoccollaboration
                                    WHERE
                                    doc_id = {obj}
                                    AND to_user IN (
                                        SELECT
                                        id
                                        FROM
                                        benutzer
                                        WHERE
                                        benutzer = '{context_user}'
                                    )
                                    AND 
                                        valid_from <= '{current_timestamp}' 
                                    AND
                                        valid_to >= '{current_timestamp}'
                                """

                sql_result = client.execute_sql(sql_command=sql_statement)

                if sql_result:
                    if len(sql_result) > 0:
                        # rights so aufbauen, dass die Access Klasse damit arbeiten kann
                        result[obj] = Access(
                            True if "R" in sql_result[0]["rights"] else False,
                            True if "W" in sql_result[0]["rights"] else False,
                            True if "X" in sql_result[0]["rights"] else False,
                            True if "D" in sql_result[0]["rights"] else False,
                            True if "U" in sql_result[0]["rights"] else False,
                        )
                    else:
                        raise RuntimeError("doc-collaboration for object not found.")
                else:
                    raise RuntimeError("doc-collaboration for object not found.")

            return result
