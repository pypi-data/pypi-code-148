# coding=utf-8
"""
FAAPIService
"""
import asyncio
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime, timedelta, tzinfo
from inspect import stack as i_stack
from json import dumps, loads, JSONDecodeError
from time import time
from traceback import format_exc
from typing import Any, Callable, Coroutine, Dict, List, Optional, Tuple, Union

import aiohttp
import bs4
from viledatools import FARequests, getcookieval


@dataclass
class HTTPClientSessionStatus:
    login_mutex: Optional[bool] = None
    login_timestamp: Optional[float] = None


class FAAPIService:
    """
    Base class to build FA API services
    """

    def __init__(self,
                 log: Callable[..., Coroutine[Any, Any, Any]],
                 vapp: str,
                 uagent: str,
                 webrelogin: int,
                 graphql: Dict[str, str] = None,
                 debuglog: bool = False):
        """
        Init the base class

        :param log: logger callable coroutine to use
        :param vapp: FA mobile API app version to use
        :param uagent: User-Agent string to use for mobile API
        :param uagent: web API relogin interval
        :param graphql: GraphQL requests, key is GraphQL method name, value is request body
        :param debuglog: enable debug logging
        """
        # Reference logging object of the caller
        self._base_log: Callable[..., Coroutine[Any, Any, Any]] = log
        # FA mobile API version
        self._vapp = vapp
        # FA mobile API standard headers to provide
        self._app_headers = {"version":    vapp,
                             "Accept":     "*/*",
                             "User-Agent": uagent
                             }
        # Web relogin interval in seconds
        self._webrelogin = float(webrelogin)
        # GraphQL requests
        self._graphql = dict()
        if isinstance(graphql, dict):
            self._graphql = graphql
        else:
            self._graphql = dict()
        # Debug logging
        self._debuglog = debuglog
        # Multiple client sessions
        self._s: Dict[str, aiohttp.ClientSession] = dict()
        self._s_status: Dict[str, HTTPClientSessionStatus] = dict()
        # FA web api time reg draw counter
        self._fa_api_draw = 1

    @staticmethod
    def fa_extract_recurrence(recurrence: Dict[str, Any],
                              taskid: int) -> List[Dict[str, Any]]:
        """
        Extracts task sequence by date from response of FA mobile API tasks request

        :param recurrence: contents of FA mobile API tasks request "recurrence"
        :param taskid: FA backend task ID
        :return: corresponding task sequence
        """
        _res = list()
        for _task_str_id in recurrence.keys():
            if int(_task_str_id) == taskid:
                for _seq_nr_str, _seq_dates_list in recurrence[_task_str_id].items():
                    _res.append({"sequenceNumber": int(_seq_nr_str),
                                 "_date_start":    _seq_dates_list[0],
                                 "_date_end":      _seq_dates_list[1]
                                 })
                return _res
        return _res

    @staticmethod
    def parse_form_html(rawhtml: str) -> Dict[str, Any]:
        """
        Parses the raw FA form submission questions page HTML into structured dict

        :param rawhtml: raw string with HTML contents
        :result: dictionary with submitted form contents
        """
        _strainer_content = bs4.SoupStrainer(name="content", id="Content")
        _bs_content = bs4.BeautifulSoup(rawhtml, features="lxml", parse_only=_strainer_content)
        _out = dict()
        for _child in _bs_content.content.children:
            if isinstance(_child,
                          bs4.element.Tag) and _child.name == "div" and "card" in _child["class"]:
                if "card-header" in _child.div["class"]:
                    _category_name = _child.div.contents[0]
                else:
                    _category_name = None
                _category_fields = list()
                if "card-body" in _child.ul["class"]:
                    for _ul_child in _child.ul:
                        _field = dict()
                        if isinstance(_ul_child,
                                      bs4.element.Tag) and _ul_child.name == "li" and "list-group-item" in _ul_child[
                                                                                                            "class"]:
                            _field["name"] = _ul_child.label.contents[0].replace(chr(10), '').strip()
                            _field["question"] = int(_ul_child.label["for"].split("question-")[1])
                            if _ul_child.div is not None:
                                _field_img = _ul_child.div.find(name="img")
                                _field_lookup = _ul_child.div.find_all(name="div", class_="lookup-table-answers")
                                if _field_img is not None and not _field_lookup:
                                    _field["type"] = "image"
                                    _field["val"] = _field_img["src"]
                                elif _field_img is None and not _field_lookup:
                                    _field["type"] = "value"
                                    _field["val"] = _ul_child.div.contents[0].replace(chr(10), '').strip()
                                elif _field_lookup:
                                    _field["type"] = "lookup"
                                    _selections = list()
                                    for _lookup in _field_lookup:
                                        _selection_item = dict()
                                        _lookup_selection = _lookup.find(name="div", class_="lookup-table-selection")
                                        _selection_item_key = _lookup_selection.contents[0].replace(chr(10), '').strip()
                                        _lookup_subanswers = _lookup.find(name="div", class_="sub-answers")
                                        # Parse subanswers into tuples
                                        _sa_names = list()
                                        _sa_vals = list()
                                        for _sa_child in _lookup_subanswers:
                                            if isinstance(_sa_child, bs4.element.Tag):
                                                if _sa_child.name == "label":
                                                    _sa_names.append(_sa_child.contents[0].replace(chr(10), '').strip())
                                                elif _sa_child.name == "div":
                                                    if _sa_child.contents:
                                                        try:
                                                            _sa_val = int(
                                                                _sa_child.contents[0].replace(chr(10), '').strip())
                                                        except ValueError:
                                                            _sa_val = _sa_child.contents[0].replace(chr(10), '').strip()
                                                        _sa_vals.append(_sa_val)
                                                    else:
                                                        _sa_vals.append(None)
                                        _lookup_subanswers_tuples = list()
                                        if len(_sa_names) == len(_sa_vals):
                                            for _i in range(len(_sa_names)):
                                                _lookup_subanswers_tuples.append((_sa_names[_i], _sa_vals[_i]))
                                        else:
                                            # Parsing exception
                                            pass
                                        _selection_item[_selection_item_key] = _lookup_subanswers_tuples
                                        _selections.append(_selection_item)
                                    _field["val"] = _selections
                            if _field:
                                _category_fields.append(_field)
                _out[_category_name] = _category_fields
        return _out

    async def faweb_login(self, domain: str, usr: str, pwd: str) -> bool:
        """
        Login to FA web API, keep session, and return True if successful

        :param domain: FA domain name
        :param usr: FA user login name
        :param pwd: FA password
        :return: True if successful, None or False if not
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        if self._s_status[_s_name].login_mutex:
            return True
        else:
            self._s_status[_s_name].login_mutex = True
        try:
            r = await self._s[_s_name].head(f"https://{domain}.facilityapps.com/login")
            await self._base_log(i_stack(),
                                 "debug",
                                 (f"OK got init XSRF-TOKEN cookie = "
                                  f"{getcookieval(self._s[_s_name], 'XSRF-TOKEN')} from {r.url.path}"))
            r = await self._s[_s_name].post(f"https://{domain}.facilityapps.com/login",
                                            data={"_token":   getcookieval(self._s[_s_name], "XSRF-TOKEN"),
                                                  "username": usr,
                                                  "password": pwd,
                                                  "submit":   str()
                                                  })
            if getcookieval(self._s[_s_name], "laravel_token"):
                # Successfully authenticated
                self._s_status[_s_name].login_mutex = False
                self._s_status[_s_name].login_timestamp = time()
                # Log the OK
                await self._base_log(i_stack(), "info", (f"OK logged in to {r.url.path} -> {r.content_type} "
                                                         f"[{r.content_length}B] redirects counted: {len(r.history)}"))
                return True
            else:
                self._s_status[_s_name].login_mutex = False
                await self._base_log(i_stack(), "error", (f"FAILED to log in web API, redirected to {r.url.path} "
                                                          f"redirects counted: {len(r.history)}"))
                return False
        except aiohttp.ClientResponseError as _badstatus:
            self._s_status[_s_name].login_mutex = False
            await self._base_log(i_stack(), "debug", f"Full failed URL: {_badstatus.request_info.url}")
            await self._base_log(i_stack(), "error", f"Error {_badstatus.request_info.method} "
                                                     f"{_badstatus.request_info.url.path} - "
                                                     f"{_badstatus.status} {_badstatus.message}")

    async def faweb_logout(self, domain: str, usr: str) -> bool:
        """
        Logout from FA web API for all accounts
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        while self._s_status[_s_name].login_mutex:
            await asyncio.sleep(1.000)
        r = await self._s[_s_name].get(f"https://{domain}.facilityapps.com/logout")
        if r.ok:
            await self._base_log(i_stack(),
                                 "info",
                                 f"OK web logout successful for user '{usr}' from domain '{domain}'")
            _res = True
        else:
            await self._base_log(i_stack(),
                                 "info",
                                 f"FAILED web logout for user '{usr}' from domain '{domain}'")
            _res = False
        await self._s[_s_name].close()
        return _res

    async def faweb_get_configview(self,
                                   domain: str,
                                   usr: str) -> Optional[Dict[str, Any]]:
        """
        Get the config parameters for enfironment for FA API domain

        :param domain: FA domain name
        :param usr: FA user login name
        :return: dict mapping user ID: site object
        """
        # Output dict
        _c = dict()
        _s_name = self._faweb_get_session_name(domain, usr)
        while self._s_status[_s_name].login_mutex:
            await asyncio.sleep(1.000)
        r = await self._s[_s_name].get(f"https://{domain}.facilityapps.com/system_configuration/view",
                                       headers={"Accept": "text/html, application/xhtml+xml"})
        if r.ok:
            _raw_html = await r.text()
        else:
            await self._base_log(i_stack(), "error",
                                 f"FAILED requesting system config for domain '{domain}' user '{usr}': "
                                 f"HTTP {r.status} {r.reason}")
            return None
        _strainer_tz = bs4.SoupStrainer(name="select", id="SystemConfiguration_timezone")
        _bs = bs4.BeautifulSoup(_raw_html, features="lxml", parse_only=_strainer_tz)
        _opts = _bs.find_all(name="option")
        for _o in _opts:
            if isinstance(_o.get("selected"), str):
                _c["tz"] = _o["value"]
        # _strainer_langs = bs4.SoupStrainer(name="select", id="SystemConfiguration_timezone")
        # bs = bs4.BeautifulSoup(await r.text(), features="lxml", parse_only=_strainer_langs)
        # _opts = bs.find_all(name="option")
        # for _o in _opts:
        #     if isinstance(_o.get("selected"), str):
        #         _c["tz"] = timezone(_o["value"])
        return _c

    async def faweb_get_timereg(self,
                                domain: str,
                                usr: str,
                                tbeg: datetime,
                                tend: datetime) -> Optional[List[Dict[str, Any]]]:
        """
        Get time registration data from the  FA web API for specified domain and time interval

        :param domain: FA domain name
        :param usr: FA user login name
        :param tbeg: date and time from which to select tasks
        :param tend: date and time till which to select tasks
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        # Check cookies
        if not isinstance(getcookieval(self._s[_s_name], "XSRF-TOKEN"), str):
            raise ValueError(f"no XSRF-TOKEN: {getcookieval(self._s[_s_name], 'XSRF-TOKEN')}")
        while self._s_status[_s_name].login_mutex:
            await asyncio.sleep(1.000)
        async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/api/1.0/time_registration/data",
                                         headers={"Accept":       "application/json",
                                                  "X-CSRF-TOKEN": getcookieval(self._s[_s_name], "XSRF-TOKEN")
                                                  },
                                         params={"fields": FARequests.timeregquery()},
                                         data=FARequests.timeregform(self._fa_api_draw,
                                                                     tbeg,
                                                                     tend)) as r:
            self._fa_api_draw += 1
            if r.status == 200:
                _json = await r.json()
                return _json["data"]
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA web API time reg data request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return list()

    async def faweb_get_graphql(self,
                                domain: str,
                                usr: str,
                                opname: str,
                                pagesize: int,
                                objecttype: type,
                                query: Optional[List[Tuple[str, str]]] = None,
                                progresscallback: Optional[Callable[[int, int, int, float, str], None]] = None,
                                attempts: int = 5,
                                retry_timeout: float = 5.0,
                                retry_multiplier: float = 3.0) -> Optional[Union[Dict[str, Any], List[Any]]]:
        """
        Request generic FA web GraphQL API and return FA data output

        :param domain: FA domain name
        :param usr: FA user login name
        :param opname: name of GraphQL request
        :param pagesize: page size to use max 500
        :param objecttype: expected response object type, use list if expected collection of objects, and dict if
                           only one object
        :param query: query parameters list, each list item is query parameter tuple (tag, value) where tag is
                      tempalte tag that will be replaced by value in the text of GraphQL request, please make tags
                      unique and following naming convention applicable to programming variables, value is any text to
                      be substituted in place of tag; reserved tag names TEMPLATE_PAGE_NUM and TEMPLATE_PAGE_SIZE,
                      using of these two tag names must be avoided, because these tags are user for pagination
        :param progresscallback: callback function, accepts four parameters:
                                 cprocessed - integer how many entities processed,
                                 csuccessful - integer how many entities successfully processed,
                                 ctotal - integer how many entities in total,
                                 cprc - float in range 0.0 to 1.0 meaning % of progress
                                 cmsg - string with arbitrary message
        :param attempts: how many times to retry, one common attempts counter works for whole request for all pages
        :param retry_timeout: timeout in seconds before first retry
        :param retry_multiplier: multiplier of timeout for each consecutive retry
        :return: list of objects loaded from FA web API response JSON in case of
        """
        _current_attempt = 1
        _retry_timeout = retry_timeout
        _s_name = self._faweb_get_session_name(domain, usr)
        try:
            progresscallback(0,
                             0,
                             0,
                             0.0,
                             f"Requesting {opname} for domain {domain}")
            if objecttype == list:
                _return: Union[Dict[str, Any], List[Any]] = list()
            elif objecttype == dict:
                _return: Union[Dict[str, Any], List[Any]] = dict()
            else:
                raise ValueError(f"wrong objecttype value: {objecttype}, only list and dict supported")
            if self._s_status[_s_name].login_timestamp is None:
                raise ValueError(f"user was not authenticated before requesting")
            if not isinstance(pagesize, int) or pagesize < 1 or pagesize > 500:
                raise ValueError(f"wrong page size = {pagesize} allowed from 1 to 500")
            if opname not in self._graphql.keys():
                raise KeyError(f"source code for GraphQL request '{opname}' not found")
            _gql_query: str = self._graphql[opname].replace("TEMPLATE_PAGE_SIZE", str(pagesize))
            if query is not None:
                for _template_item in query:
                    _gql_query = _gql_query.replace(_template_item[0], _template_item[1])
            # Check cookies
            if not isinstance(getcookieval(self._s[_s_name], "XSRF-TOKEN"), str):
                raise ValueError(f"no XSRF-TOKEN: {getcookieval(self._s[_s_name], 'XSRF-TOKEN')}")
            # Request by pages
            _page_num = 1
            _records_total: Optional[int] = None
            _r_json_no_paginator = True
            while _records_total is None or len(_return) < _records_total:
                while self._s_status[_s_name].login_mutex:
                    await asyncio.sleep(1.000)
                r = await self._s[_s_name].post(f"https://{domain}.facilityapps.com/api/graphql",
                                                headers={"Accept":          "application/json",
                                                         "Origin":          f"https://{domain}.facilityapps.com",
                                                         "Accept-Encoding": "gzip, deflate",
                                                         "Accept-Language": "*",
                                                         "Content-Type":    "application/json",
                                                         "Sec-Fetch-Dest":  "empty",
                                                         "Sec-Fetch-Mode":  "cors",
                                                         "Sec-Fetch-Site":  "same-origin",
                                                         "TE":              "gzip"
                                                         },
                                                data=dumps({"operationName": opname,
                                                            "query": _gql_query.replace("TEMPLATE_PAGE_NUM",
                                                                                        str(_page_num)),
                                                            "variables": {}}, ensure_ascii=False).encode("utf-8"))
                _response_payload = await r.read()
                _response_timestamp = time()
                if _response_payload:
                    _response_content = {r.headers["Content-Type"]: _response_payload.decode("utf-8")}
                else:
                    _response_content = None
                if r.ok and _response_payload:
                    _r_json_ok = False
                    _r_json_data: Optional[List[Any]] = None
                    _r_json_paginator: Optional[Dict[str, int]] = None
                    with suppress(JSONDecodeError):
                        _r_json = loads(_response_payload.decode("utf-8"))
                        if "data" in _r_json.keys():
                            if isinstance(_r_json["data"], dict) and len(_r_json["data"]) > 0:
                                _r_json_val0 = list(_r_json["data"].values())[0]
                                if isinstance(_r_json_val0, dict):
                                    if objecttype == list and "data" in _r_json_val0.keys():
                                        if isinstance(_r_json_val0["data"], list):
                                            if "paginatorInfo" in _r_json_val0.keys():
                                                _r_json_data = _r_json_val0["data"]
                                                _r_json_pg = _r_json_val0["paginatorInfo"]
                                                _r_json_ok = True
                                                for _r_json_data_item in _r_json_data:
                                                    if isinstance(_r_json_data_item, dict):
                                                        _r_json_data_item["__response_timestamp"] = _response_timestamp
                                                _return += _r_json_data
                                                if isinstance(_r_json_pg, dict) and "total" in _r_json_pg.keys():
                                                    if isinstance(_r_json_pg["total"], int):
                                                        if _records_total is None:
                                                            _records_total = _r_json_pg["total"]
                                                            _r_json_no_paginator = False
                                                        else:
                                                            if _r_json_pg["total"] != _records_total:
                                                                raise ValueError(f"request cancelled: total number of"
                                                                                 f" records changed while paginating"
                                                                                 f" - was {_records_total}"
                                                                                 f" became {_r_json_pg['total']}")
                                    elif objecttype == dict:
                                        if len(_r_json_val0) > 0:
                                            _return = list(_r_json_val0.values())[0]
                                            if isinstance(_return, dict):
                                                _return["__response_timestamp"] = _response_timestamp
                                            _r_json_ok = True
                                    else:
                                        raise ValueError(f"wrong object in response from API"
                                                         f" for expected type {objecttype}")
                    if _r_json_ok:
                        if objecttype == dict:
                            if self._debuglog:
                                await self._base_log(i_stack(),
                                                     "debug",
                                                     (f"OK FA web API GraphQL request {opname}"
                                                      f" at page number {_page_num} / page size {pagesize}"
                                                      f" domain '{domain}' user '{usr}' {len(_return)}"
                                                      f" total records received"),
                                                     logo=_response_content)
                            progresscallback(1,
                                             1,
                                             1,
                                             1.0,
                                             f"Requesting {opname} for domain {domain}")
                            break
                        if _r_json_no_paginator:
                            if self._debuglog:
                                await self._base_log(i_stack(),
                                                     "debug",
                                                     (f"FA web API GraphQL request {opname} no paginatorInfo received"
                                                      f" at page number {_page_num} / page size {pagesize}"
                                                      f" domain '{domain}' user '{usr}' break and return "
                                                      f" with only {len(_return)} records received"),
                                                     logo=_response_content)
                            progresscallback(len(_return),
                                             len(_return),
                                             len(_return),
                                             1.0,
                                             f"Requesting {opname} for domain {domain}")
                            break
                        else:
                            if self._debuglog:
                                await self._base_log(i_stack(),
                                                     "debug",
                                                     (f"OK FA web API GraphQL request {opname}"
                                                      f" at page number {_page_num} / page size {pagesize}"
                                                      f" domain '{domain}' user '{usr}' {len(_return)}"
                                                      f" total records received"),
                                                     logo=_response_content)
                            _page_num += 1
                            _retry_timeout = retry_timeout
                            progresscallback(len(_return),
                                             len(_return),
                                             _records_total,
                                             len(_return) / _records_total if _records_total > 0 else 1.0,
                                             f"Requesting {opname} for domain {domain}")
                    else:
                        await self._base_log(i_stack(),
                                             "warning",
                                             (f"FAILED FA web API GraphQL request {opname} wrong response content"
                                              f" at page number {_page_num} / page size {pagesize}"
                                              f" domain '{domain}' user '{usr}'"),
                                             logo=_response_content)
                        return None
                else:
                    await self._base_log(i_stack(),
                                         "warning",
                                         (f"FAILED FA web API GraphQL request {opname} page number {_page_num}"
                                          f" / page size {pagesize} domain '{domain}' user '{usr}'"
                                          f" attempt {_current_attempt}: HTTP {r.status} {r.reason}"),
                                         logo=_response_content)
                    if _current_attempt < attempts:
                        _current_attempt += 1
                        await asyncio.sleep(_retry_timeout)
                        _retry_timeout *= retry_multiplier
                    else:
                        return None
            return _return
        except asyncio.exceptions.CancelledError:
            pass
        except Exception as _exc:
            await self._base_log(i_stack(),
                                 "error",
                                 (f"FAILED faweb_get_graphql() request {opname} domain '{domain}' user '{usr}':"
                                  f" {format_exc().replace(chr(10), ' ')}"),
                                 exc=_exc,
                                 fexc=format_exc())
            return None

    async def faweb_get_tasks(self,
                              domain: str,
                              usr: str,
                              siteid: int,
                              td: datetime) -> Optional[Dict[str, Any]]:
        """
        Gets all tasks from FA web API for specified domain, date and specified site ID

        :param domain: FA domain name
        :param usr: FA user login name
        :param siteid: FA backend site ID
        :param td: date for which to select tasks
        :return: dict loaded from FA web API response JSON
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        try:
            # Check cookies
            if not isinstance(getcookieval(self._s[_s_name], "XSRF-TOKEN"), str):
                raise ValueError(f"no XSRF-TOKEN: {getcookieval(self._s[_s_name], 'XSRF-TOKEN')}")
            # Get all tasks
            _json_form = {"year": str(td.year),
                          "month": str(td.month),
                          "day": str(td.day),
                          "CurrentView": "day",
                          "sites[]": str(siteid),
                          "useDates": "0",
                          "includeExceptions": "true"}
            while self._s_status[_s_name].login_mutex:
                await asyncio.sleep(1.000)
            async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/api/1.0/planning/planning_data",
                                             headers={
                                                "Accept":          "application/json",
                                                "Origin":          f"https://{domain}.facilityapps.com",
                                                "Accept-Encoding": "gzip, deflate",
                                                "Accept-Language": "*",
                                                "X-CSRF-TOKEN":    getcookieval(self._s[_s_name], "XSRF-TOKEN"),
                                                "Referer":         f"https://{domain}.facilityapps.com/planning/view",
                                                "Sec-Fetch-Dest":  "empty",
                                                "Sec-Fetch-Mode":  "cors",
                                                "Sec-Fetch-Site":  "same-origin"
                                             },
                                             data=_json_form) as r:
                if r.status == 200:
                    _json_response = await r.json()
                    if "exceptions" in _json_response.keys() and _json_response["exceptions"]:
                        await self._base_log(i_stack(),
                                             "info",
                                             f"got exception field in FA API /api/1.0/planning/planning_data "
                                             f"response JSON - domain '{domain}' user '{usr}'",
                                             logo=_json_response["exceptions"])
                    return _json_response
                else:
                    await self._base_log(i_stack(), "warning",
                                         f"FAILED FA API /api/1.0/planning/planning_data request - "
                                         f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}")
                    return None
        except Exception as _exc:
            await self._base_log(i_stack(), "error", f"FAILED faweb_get_tasks(): {format_exc().replace(chr(10), ' ')}")
            return None

    async def faweb_send_push(self,
                              domain: str,
                              usr: str,
                              useridlist: List[int],
                              msg: str) -> None:
        """
        Gets all tasks for domain from FA web API for specified period

        :param domain: FA domain name
        :param usr: FA user login name
        :param useridlist: list of FA user IDs to whom to send push
        :param msg: message to send
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        try:
            if not isinstance(getcookieval(self._s[_s_name], "XSRF-TOKEN"), str):
                raise ValueError(f"no XSRF-TOKEN: {getcookieval(self._s[_s_name], 'XSRF-TOKEN')}")
            _push_json_content = dumps({"message": msg,
                                        "users": useridlist,
                                        "everyone": False},
                                       ensure_ascii=False)
            while self._s_status[_s_name].login_mutex:
                await asyncio.sleep(1.000)
            r = await self._s[_s_name].post(f"https://{domain}.facilityapps.com/api/1.0/push-messaging/send",
                                            headers={"Content-Type": "application/json; charset=utf-8",
                                                     "Accept":       "application/json",
                                                     "X-CSRF-TOKEN": getcookieval(self._s[_s_name], "XSRF-TOKEN")
                                                     },
                                            data=_push_json_content)
            if r.ok:
                pass
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA web API push message send request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason} - "
                                      f"request content was: {_push_json_content}"))
        except Exception as _exc:
            await self._base_log(i_stack(), "error", f"FAILED faweb_send_push(): {format_exc().replace(chr(10), ' ')}")

    async def faweb_update_duration(self,
                                    domain: str,
                                    usr: str,
                                    taskid: int,
                                    taskseq: int,
                                    d: timedelta) -> None:
        """
        Gets all tasks for domain from FA web API for specified period

        :param domain: FA domain name
        :param usr: FA user login name
        :param taskid: FA backend task ID
        :param taskseq: FA backend task sequence number
        :param d: duration to set
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        try:
            if not isinstance(getcookieval(self._s[_s_name], "XSRF-TOKEN"), str):
                raise ValueError(f"no XSRF-TOKEN: {getcookieval(self._s[_s_name], 'XSRF-TOKEN')}")
            _json = {"id":                   str(taskid),
                     "sequence_number":      str(taskseq),
                     "_token":               getcookieval(self._s[_s_name], "XSRF-TOKEN"),
                     "duration_hour":        str((d.seconds // 60) // 60),
                     "duration_minute":      str((d.seconds // 60) % 60),
                     "duration_second":      str(d.seconds % 60),
                     "editMode":             "single",
                     "excludeExceptions":    "",
                     "task_complete_emails": 0,
                     "task_canceled_emails": 0
                     }
            while self._s_status[_s_name].login_mutex:
                await asyncio.sleep(1.000)
            r = await self._s[_s_name].post(f"https://{domain}.facilityapps.com/api/1.0/planning/save",
                                            headers={"Accept":       "application/json",
                                                     "Content-Type": "application/json; charset=utf-8",
                                                     "X-CSRF-TOKEN": getcookieval(self._s[_s_name], "XSRF-TOKEN")
                                                     },
                                            data=dumps(_json, ensure_ascii=False))
            if r.ok:
                _res = await r.json()
                if "result" not in _res.keys() or _res["result"] is not True:
                    await self._base_log(i_stack(), "warning", f"FAILED FA web API update duration request - "
                                                               f"domain '{domain}' user '{usr}': API response = {_res}")
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA web API update duration request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
        except Exception as _exc:
            await self._base_log(i_stack(), "error",
                                 f"FAILED faweb_update_duration(): {format_exc().replace(chr(10), ' ')}")

    async def faweb_get_submitted_forms(self,
                                        domain: str,
                                        usr: str,
                                        tbeg: datetime,
                                        tend: datetime) -> Optional[List[Dict[str, Any]]]:
        """
        Gets all submitted forms for domain from FA web API for specified period

        :param domain: FA domain name
        :param usr: FA user login name
        :param tbeg: date and time from which to select tasks
        :param tend: date and time till which to select tasks
        :return: dict loaded from FA web API response JSON
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        try:
            # Check cookies
            if not isinstance(getcookieval(self._s[_s_name], "XSRF-TOKEN"), str):
                raise ValueError(f"no XSRF-TOKEN: {getcookieval(self._s[_s_name], 'XSRF-TOKEN')}")
            # Get all submitted forms
            while self._s_status[_s_name].login_mutex:
                await asyncio.sleep(1.000)
            r = await self._s[_s_name].post((f"https://{domain}.facilityapps.com"
                                             f"/api/1.0/forms/reporting?fields={FARequests.formsreportingquery()}"),
                                            headers={"Accept":       "application/json",
                                                     "X-CSRF-TOKEN": getcookieval(self._s[_s_name], "XSRF-TOKEN")
                                                     },
                                            data=FARequests.formsreportingform(1, tbeg, tend))
            if r.ok:
                _forms_list_json = await r.json()
                return _forms_list_json["data"]
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA web API submitted forms list request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return None
        except Exception as _exc:
            await self._base_log(i_stack(), "error", f"FAILED faweb_get_submitted_forms(): "
                                                     f"{format_exc().replace(chr(10), ' ')}")
            return None

    async def faweb_get_form_details(self,
                                     domain: str,
                                     usr: str,
                                     submissionid: int) -> Optional[Dict[str, Any]]:
        """
        Get submitted form details and parse with parse_form_html()

        :param domain: FA domain name
        :param usr: FA user login name
        :param submissionid: ID of form submission
        :return: dictionary with submitted form contents
        """
        # Output dict
        _out = dict()
        _s_name = self._faweb_get_session_name(domain, usr)
        while self._s_status[_s_name].login_mutex:
            await asyncio.sleep(1.000)
        r = await self._s[_s_name].get(f"https://{domain}.facilityapps.com/forms/submission/view/{submissionid}",
                                       headers={"Accept": "text/html, application/xhtml+xml"})
        if r.ok:
            _raw_html = await r.text()
        else:
            await self._base_log(i_stack(), "error",
                                 f"FAILED requesting details for form submission id = {submissionid} for "
                                 f"domain '{domain}' user '{usr}': "
                                 f"HTTP {r.status} {r.reason}")
            return None
        return self.parse_form_html(_raw_html)

    async def faapp_login(self, domain: str, usr: str, pwd: str) -> Optional[Dict[str, Any]]:
        """
        Login to FA mobile app API and return the main user record

        :param domain: FA domain name
        :param usr: FA user login name
        :param pwd: FA password
        :return: dict with FA user full record
        """
        _form = {"T":           "LogIn_v2",
                 "username":    usr,
                 "password":    pwd,
                 "version":     self._vapp,
                 "mode":        "LogIn",
                 "auth_method": "basic"
                 }
        _s_name = self._faapp_get_session_name(domain, usr)
        async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/FacilityAppsAPI.php",
                                         headers=self._app_headers,
                                         data=_form) as r:
            if r.status == 200:
                _json = await r.json()
                return _json
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA mobile API login request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return None

    async def faapp_get_forms(self, domain: str, usr: str, language: str, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Call FA mobile API GetChecklists and return result

        :param domain: FA domain name
        :param usr: FA user login name
        :param language: language code in form of en_EN to use for language and region form fields
        :param session_id: FA mobile API session_id
        :return: dict with FA API output of GetChecklists
        """
        _form = {"session_id":  session_id,
                 "T":           "GetChecklists",
                 "L":           language,
                 "region_code": language
                 }
        _s_name = self._faapp_get_session_name(domain, usr)
        async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/FacilityAppsAPI.php",
                                         headers=self._app_headers,
                                         data=_form) as r:
            if r.status == 200:
                _json = await r.json()
                return _json
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA API GetChecklists request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return None

    async def faapp_task_begin(self,
                               domain: str,
                               usr: str,
                               language: str,
                               session_id: str,
                               siteid: int,
                               taskid: int,
                               taskseq: int,
                               stime: datetime) -> bool:
        """
        Set task to begin

        :param domain: FA domain name
        :param usr: FA user login name
        :param language: language code in form of en_EN to use for language and region form fields
        :param session_id: FA mobile API session_id
        :param siteid: FA backend site ID
        :param taskid: FA backend task ID
        :param taskseq: FA backend task sequence number
        :param stime: date and time to set status at
        :return: True if successful
        """
        _form = {"T":                "StartProgressOnTask",
                 "L":                language,
                 "FormData":         dumps({"task_id":            str(taskid),
                                            "sequence_number":    taskseq,
                                            "time_of_change":     str(int(stime.timestamp())),
                                            "latitude":           None,
                                            "longitude":          None,
                                            "time_registrations": None
                                            }, ensure_ascii=False),
                 "ReferenceId":      siteid,
                 "ReferenceType":    1,
                 "Timestamp":        int(stime.timestamp()),
                 "session_id":       session_id,
                 "AppVersionNumber": self._vapp,
                 "TaskData":         "null"
                 }
        _s_name = self._faapp_get_session_name(domain, usr)
        async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/FacilityAppsAPI.php",
                                         headers=self._app_headers,
                                         data=_form) as r:
            if r.status == 200:
                _json = await r.json()
                return _json
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA API StartProgressOnTask request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return False

    async def faapp_task_set_status(self,
                                    domain: str,
                                    usr: str,
                                    session_id: str,
                                    taskid: int,
                                    taskseq: int,
                                    status: int,
                                    stime: datetime) -> bool:
        """
        Set status to task

        :param domain: FA domain name
        :param usr: FA user login name
        :param session_id: FA mobile API session_id
        :param taskid: FA backend task ID
        :param taskseq: FA backend task sequence number
        :param status: integer FA backend status to set
        :param stime: date and time to set status at
        :return: True if successful
        """
        _form = {"T":               "SetCalendarSubStatus",
                 "task_id":         taskid,
                 "sequence_number": taskseq,
                 "option":          status,
                 "latitude":        str(),
                 "longitude":       str(),
                 "timestamp":       int(stime.timestamp()),
                 "extra":           '{"clock_log_list":null}',
                 "session_id":      session_id
                 }
        _s_name = self._faapp_get_session_name(domain, usr)
        async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/FacilityAppsAPI.php",
                                         headers=self._app_headers,
                                         data=_form) as r:
            if r.status == 200:
                _json = await r.json()
                return _json
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA API SetCalendarSubStatus request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return False

    async def faapp_task_chat(self,
                              domain: str,
                              usr: str,
                              language: str,
                              session_id: str,
                              siteid: int,
                              taskid: int,
                              taskseq: int,
                              msg: str,
                              fauserid: int,
                              dtz: tzinfo) -> bool:
        """
        Send chat message to the task

        :param domain: FA domain name
        :param usr: FA user login name
        :param language: language code in form of en_EN to use for language and region form fields
        :param session_id: FA mobile API session_id
        :param siteid: FA backend site ID
        :param taskid: FA backend task ID
        :param taskseq: FA backend task sequence number
        :param msg: text message to append to chat
        :param fauserid: FA user id under which to send message
        :param dtz: tzinfo time zone of the domain
        :return: True if successful
        """
        _time = int(time())
        _time_tz = datetime.fromtimestamp(_time, dtz)
        _form = {"T":                "SaveTaskMessage",
                 "L":                language,
                 "FormData":         dumps({"id":              0,
                                            "task_id":         taskid,
                                            "subtask_id":      None,
                                            "sequence_number": taskseq,
                                            "message":         msg,
                                            "user":            str(fauserid),
                                            "timestamp":       _time_tz.strftime("%Y-%m-%d %H:%M:%S"),
                                            "images":          []
                                            }, ensure_ascii=False),
                 "ReferenceId":      siteid,
                 "ReferenceType":    1,
                 "Timestamp":        _time,
                 "session_id":       session_id,
                 "AppVersionNumber": self._vapp,
                 "TaskData":         "null"
                 }
        _s_name = self._faapp_get_session_name(domain, usr)
        async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/FacilityAppsAPI.php",
                                         headers=self._app_headers,
                                         data=_form) as r:
            if r.status == 200:
                _json = await r.json()
                return _json
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA API StartProgressOnTask request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return False

    async def faapp_task_drop_begin(self,
                                    domain: str,
                                    usr: str,
                                    language: str,
                                    session_id: str,
                                    siteid: int,
                                    taskid: int,
                                    taskseq: int,
                                    stime: datetime) -> bool:
        """
        Set task back to blue open state

        :param domain: FA domain name
        :param usr: FA user login name
        :param language: language code in form of en_EN to use for language and region form fields
        :param session_id: FA mobile API session_id
        :param siteid: FA backend site ID
        :param taskid: FA backend task ID
        :param taskseq: FA backend task sequence number
        :param stime: date and time to set status at
        :return: True if successful
        """
        _form = {"T":                "TaskToBacklog",
                 "L":                language,
                 "FormData":         dumps({"task_id":            str(taskid),
                                            "sequence_number":    taskseq,
                                            "time_of_change":     str(int(stime.timestamp())),
                                            "latitude":           None,
                                            "longitude":          None,
                                            "time_registrations": list()
                                            }, ensure_ascii=False),
                 "ReferenceId":      siteid,
                 "ReferenceType":    1,
                 "Timestamp":        int(stime.timestamp()),
                 "session_id":       session_id,
                 "AppVersionNumber": self._vapp,
                 "TaskData":         "null"
                 }
        _s_name = self._faapp_get_session_name(domain, usr)
        async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/FacilityAppsAPI.php",
                                         headers=self._app_headers,
                                         data=_form) as r:
            if r.status == 200:
                _json = await r.json()
                return _json
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA API TaskToBacklog request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return False

    async def faapp_get_tasks(self,
                              domain: str,
                              usr: str,
                              session_id: str,
                              tbeg: datetime,
                              tend: datetime,
                              language: str,
                              sitelist: List[int]) -> Optional[Dict[str, Any]]:
        """
        Gets all tasks for domain from FA mobile API for specified period

        :param domain: FA domain name
        :param usr: FA user login name
        :param session_id: FA mobile API session_id
        :param tbeg: date and time from which to select tasks
        :param tend: date and time till which to select tasks
        :param language: language code in form of en_EN to use for language and region form fields
        :param sitelist: list of integer FA backend site IDs
        :return: dict loaded from FA web API response JSON
        """
        _s_name = self._faapp_get_session_name(domain, usr)
        try:
            _json = {"CurrentView":       "custom",
                     "start":             tbeg.strftime("%Y-%m-%d"),
                     "end":               tend.strftime("%Y-%m-%d"),
                     "sites":             sitelist,
                     "includeExceptions": True,
                     "region_code":       language
                     }
            async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/api/1.0/planning/planning_data",
                                             headers={**self._app_headers,
                                                      **{"Content-Type":  "application/json; charset=utf-8",
                                                         "Authorization": f"Bearer {session_id}"
                                                         }
                                                      },
                                             data=dumps(_json, ensure_ascii=False)) as r:
                if r.status == 200:
                    _json_response = await r.json()
                    if "exceptions" in _json_response.keys() and _json_response["exceptions"]:
                        await self._base_log(i_stack(),
                                             "info",
                                             f"got exception field in FA API /api/1.0/planning/planning_data "
                                             f"response JSON - domain '{domain}' user '{usr}'",
                                             logo=_json_response["exceptions"])
                    return _json_response
                else:
                    await self._base_log(i_stack(), "warning",
                                         f"FAILED FA API /api/1.0/planning/planning_data request - "
                                         f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}")
                    return None
        except Exception as _exc:
            await self._base_log(i_stack(), "error", str(), _exc, format_exc())
            return None

    def _faapp_get_session_name(self, domain: str, usr: str) -> str:
        """
        Generate aiohttp session name and create the session itself for FA mobile API to persist it

        :param domain: FA domain name
        :param usr: FA user login name
        :return: generated aiohttp session name to persiste the session in self._s
        """
        _s_name = f"app-{domain}-{usr}".lower()
        if _s_name not in self._s.keys():
            self._s[_s_name] = aiohttp.ClientSession()
            self._s_status[_s_name] = HTTPClientSessionStatus(None, None)
        return _s_name

    def _faweb_get_session_name(self, domain: str, usr: str) -> str:
        """
        Generate aiohttp session name and create the session itself for FA web API to persist it

        :param domain: FA domain name
        :param usr: FA user login name
        :return: generated aiohttp session name to persiste the session in self._s
        """
        _s_name = f"web-{domain}-{usr}".lower()
        if _s_name not in self._s.keys():
            self._s[_s_name] = aiohttp.ClientSession()
        if _s_name not in self._s_status.keys():
            self._s_status[_s_name] = HTTPClientSessionStatus(None, None)
        return _s_name
