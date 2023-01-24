import pytest

from m360.utils import to_json
from m360.user import instance as user_instance
from m360.rbac import instance as rbac_instance
from .helper import Request

user = user_instance()
rbac = rbac_instance()

def build_request(m360_header=None):
    if m360_header:
        return Request(headers={"m360": m360_header})

    return Request(headers={
        "m360": to_json({
            "API": {
                "method": "get",
                "endpoint": "/"
            },
            "user": {
                "id": "12345",
                "username": "owner",
                "email": "mike@corsairm360.com",
                "account": {
                    "_id": "6041ed8e08acbf71381e0789",
                    "name": "mikeorg",
                }
            },
            "rbac": {
                "fields": {
                    "operator": "allow",
                    "list": {
                        "first": "firstName",
                        "username": "username",
                        "account": "account",
                        "config": "config.M360.common.pet"
                    }
                },
                "resources": {
                    "mode": "own",
                    "field": "account",
                    "value": "account._id"
                },
                "conditions": {
                    "operator": "$and",
                    "criteria": [
                        {
                            "function": "EQ",
                            "arguments": {
                                "field": "username",
                                "value": "username",
                                "custom": ""
                            }
                        }, {
                            "function": "EQ",
                            "arguments": {
                                "field": "account",
                                "value": "account._id",
                                "custom": ""
                            }
                        }, {
                            "function": "EQ",
                            "arguments": {
                                "field": "username",
                                "value": "custom",
                                "custom": "owner"
                            }
                        }, {
                            "function": "EQ",
                            "arguments": {
                                "field": "config.M360.common.primary",
                                "value": "custom",
                                "custom": "true"
                            }
                        }
                    ]
                }
            }
        })
    })

def test_set_service_config_1():
    rbac.set_service_config({
        "contract": {
            "name": "express",
            "group": "Testing",
            "version": 1,
            "ports": {
                "data": 4002,
                "maintenance": 4002
            },
            "apis": {
                "main": {
                    "get": {
                        "/": {
                            "label": "get api",
                            "access": True,
                            "rbac": {
                                "fields": ["config"]
                            }
                        }
                    },
                    "post": {
                        "/": {
                            "access": False,
                            "label": "post api",
                            "rbac": {
                                "fields": ["config"]
                            }
                        }
                    }
                }
            }
        }
    })

def test_can_access_fail_invalid():
    with pytest.raises(Exception) as e:
        rbac.can_access(build_request(to_json({
            "API": {
                "method": "get",
                "endpoint": "/"
            },
            "rbac": {
                "fields": {}
            }
        })), "invalid", {})
    assert e

def test_get_fail_no_m360():
    rb = rbac.get(Request(headers={}))
    assert not rb

def test_get_fail_m360_not_json():
    rb = rbac.get(build_request("invalid"))
    assert not rb

def test_get_fail_m360_missing_rbac():
    rb = rbac.get(build_request("{}"))
    assert not rb

def test_get_success():
    request = build_request()
    rb = rbac.get(request)
    assert rb
    assert rb.get("fields")
    assert rb.get("resources")
    assert rb.get("conditions")

    rbac_options_1 = ["fields", "field"]
    rbac_options_2 = ["resources", "resource"]
    rbac_options_3 = ["conditions", "condition"]

    for option in rbac_options_1:
        fields = rbac.get(request, option)
        assert fields.get("operator")
        assert fields.get("list")
    for option in rbac_options_2:
        resources = rbac.get(request, option)
        assert resources.get("mode")
        assert resources.get("field")
        assert resources.get("value")
    for option in rbac_options_3:
        conditions = rbac.get(request, option)
        assert conditions.get("operator")
        assert conditions.get("criteria")

    with pytest.raises(Exception) as e:
        rbac.get(request, "invalid")
    assert e

def test_can_access_fields_fail_invalid_data():
    with pytest.raises(Exception) as e:
        rbac.can_access(build_request(to_json({
            "API": {
                "method": "get",
                "endpoint": "/"
            },
            "rbac": {
                "fields": {}
            }
        })), "fields", "string")
    assert e

def test_can_access_fields_success_no_rbac_configured():
    status = rbac.can_access(build_request(to_json({
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "fields": {
                "operator": None
            }
        }
    })), "fields", {"foo": "bar"})
    assert status

def test_can_access_fields_success():
    data = {
        "user": "john",
        "isAdmin": True,
        "age": 32,
        "patt": "^[a-z]+$",
        "c": {
            "c": {
                "a": "b"
            }
        },
        "d": [
            ["a", "b"],
            ["c", "d"]
        ],
        "e": [
            {"a": "b"}
        ],
        "f": {
            "abc": {
                "access": ["admin", "vip"]
            }
        },
        "g": {
            "array": [
                {
                    "a": "b"
                },
                {
                    "g": "e"
                }
            ]
        }
    }
    tests1 = [
        {"entry1": "user"},
        {"entry2": "c.c.a"},
        {"entry3": "d.[1].[0]"},
        {"entry3": "d.[0].[0]"},
        {"entry4": "e.[0].a"},
        {"entry5": "f.abc.access.[0]"},
        {"entry6": "g.array.[0].a"},
        {"entry6": "g.array.[1].g"}
    ]
    tests2 = [
        {"entry6": "g.array.[1].f"}
    ]
    tests3 = [
        {"entry6": "g.array.[1].g"}
    ]

    def go(operator, tests, status_check, option):
        options = {"operator": operator, "list": {}}
        for test in tests:
            options["list"] = test
            status = rbac.can_access(build_request(to_json({
                "API": {
                    "method": "get",
                    "endpoint": "/"
                },
                "rbac": {
                    "fields": options
                }
            })), option, data)
            assert status == status_check

    go("allow", tests1, True, "fields")
    go("deny", tests2, True, "field")
    go("deny", tests3, True, "field")

def test_can_access_resources_fail_invalid_data():
    with pytest.raises(Exception) as e:
        rbac.can_access(build_request(to_json({
            "API": {
                "method": "get",
                "endpoint": "/"
            },
            "rbac": {
                "resources": {}
            }
        })), "resources", "string")
    assert e

def test_can_access_resources_success_no_rbac_configured():
    status = rbac.can_access(build_request(to_json({
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "resources": {
                "mode": None
            }
        }
    })), "resources", {"foo": "bar"})
    assert status

def test_can_access_resources_fail_no_user():
    status = rbac.can_access(build_request(to_json({
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "resources": {
                "mode": "any"
            }
        }
    })), "resources", {"foo": "bar"})
    assert not status

def test_can_access_resources_success_any():
    status = rbac.can_access(build_request(to_json({
        "user": {
            "id": "12345",
            "username": "owner",
            "email": "mike@corsairm360.com",
            "account": {
                "_id": "6041ed8e08acbf71381e0789",
                "name": "mikeorg",
            }
        },
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "resources": {
                "mode": "any"
            }
        }
    })), "resources", {"foo": "bar"})
    assert status

def test_can_access_resources_success_own():
    status = rbac.can_access(build_request(to_json({
        "user": {
            "id": "12345",
            "username": "owner",
            "email": "mike@corsairm360.com",
            "account": {
                "_id": "6041ed8e08acbf71381e0789",
                "name": "mikeorg",
            }
        },
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "resources": {
                "mode": "own",
                "field": "account",
                "value": "account._id"
            }
        }
    })), "resource", {
        "id": "12345",
        "username": "owner",
        "email": "mike@corsairm360.com",
        "account": "6041ed8e08acbf71381e0789"
    })
    assert status

def test_can_access_conditions_fail_invalid_data():
    with pytest.raises(Exception) as e:
        rbac.can_access(build_request(to_json({
            "API": {
                "method": "get",
                "endpoint": "/"
            },
            "rbac": {
                "conditions": {}
            }
        })), "conditions", "string")
    assert e

def test_can_access_conditions_success_no_rbac_configured():
    status = rbac.can_access(build_request(to_json({
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "conditions": {
                "operator": "$and"
            }
        }
    })), "conditions", {"foo": "bar"})
    assert status

def test_can_access_conditions_fail_no_user():
    status = rbac.can_access(build_request(to_json({
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "conditions": {
                "operator": "$and",
                "criteria": [
                    {
                        "function": "EQ",
                        "arguments": {
                            "field": "username",
                            "value": "username",
                            "custom": ""
                        }
                    },
                    {
                        "function": "EQ",
                        "arguments": {
                            "field": "account",
                            "value": "account._id",
                            "custom": ""
                        }
                    },
                    {
                        "function": "EQ",
                        "arguments": {
                            "field": "username",
                            "value": "custom",
                            "custom": "owner"
                        }
                    },
                    {
                        "function": "EQ",
                        "arguments": {
                            "field": "config.M360.common.primary",
                            "value": "custom",
                            "custom": "true"
                        }
                    }
                ]
            }
        }
    })), "conditions", {"foo": "bar"})
    assert not status

def test_can_access_conditions_success_and():
    status = rbac.can_access(build_request(to_json({
        "user": {
            "id": "12345",
            "username": "owner",
            "email": "mike@corsairm360.com",
            "account": {
                "_id": "6041ed8e08acbf71381e0789",
                "name": "mikeorg",
            }
        },
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "conditions": {
                "operator": "$and",
                "criteria": [
                    {
                        "function": "EMPTY",
                        "arguments": {
                            "field": "password",
                            "value": "",
                            "custom": ""
                        }
                    },
                    {
                        "function": "NOT_EMPTY",
                        "arguments": {
                            "field": "username",
                            "value": "",
                            "custom": ""
                        }
                    },
                    {
                        "function": "EQ",
                        "arguments": {
                            "field": "account",
                            "value": "account._id",
                            "custom": ""
                        }
                    },
                    {
                        "function": "EQ",
                        "arguments": {
                            "field": "primary",
                            "value": "custom",
                            "custom": "true"
                        }
                    },
                    {
                        "function": "EQ",
                        "arguments": {
                            "field": "username",
                            "value": "custom",
                            "custom": "owner"
                        }
                    },
                    {
                        "function": "NOT_EQ",
                        "arguments": {
                            "field": "username",
                            "value": "custom",
                            "custom": "mike"
                        }
                    },
                    {
                        "function": "START",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "mi"
                        }
                    },
                    {
                        "function": "NOT_START",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "jj"
                        }
                    },
                    {
                        "function": "END",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "ke"
                        }
                    },
                    {
                        "function": "NOT_END",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "jj"
                        }
                    },
                    {
                        "function": "CONTAIN",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "ik"
                        }
                    },
                    {
                        "function": "NOT_CONTAIN",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "jj"
                        }
                    },
                    {
                        "function": "IN",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "ik"
                        }
                    },
                    {
                        "function": "NOT_IN",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "jj"
                        }
                    }
                ]
            }
        }
    })), "conditions", {
        "id": "12345",
        "username": "owner",
        "email": "mike@corsairm360.com",
        "account": "6041ed8e08acbf71381e0789",
        "primary": True,
        "config": {
            "test": "mike"
        }
    })
    assert status

def test_can_access_conditions_success_or():
    status = rbac.can_access(build_request(to_json({
        "user": {
            "id": "12345",
            "username": "owner",
            "email": "mike@corsairm360.com",
            "account": {
                "_id": "6041ed8e08acbf71381e0789",
                "name": "mikeorg",
            }
        },
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "conditions": {
                "operator": "$or",
                "criteria": [
                    {
                        "function": "EMPTY",
                        "arguments": {
                            "field": "password",
                            "value": "",
                            "custom": ""
                        }
                    },
                    {
                        "function": "EMPTY",
                        "arguments": {
                            "field": "username",
                            "value": "",
                            "custom": ""
                        }
                    }
                ]
            }
        }
    })), "conditions", {
        "id": "12345",
        "username": "owner",
        "email": "mike@corsairm360.com",
        "account": "6041ed8e08acbf71381e0789",
        "primary": True,
        "config": {
            "test": "mike"
        }
    })
    assert status

def test_can_access_conditions_fail_and():
    status = rbac.can_access(build_request(to_json({
        "user": {
            "id": "12345",
            "username": "owner",
            "email": "mike@corsairm360.com",
            "account": {
                "_id": "6041ed8e08acbf71381e0789",
                "name": "mikeorg",
            }
        },
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "conditions": {
                "operator": "$and",
                "criteria": [
                    {
                        "function": "EMPTY",
                        "arguments": {
                            "field": "username",
                            "value": "",
                            "custom": ""
                        }
                    },
                    {
                        "function": "NOT_EMPTY",
                        "arguments": {
                            "field": "password",
                            "value": "",
                            "custom": ""
                        }
                    },
                    {
                        "function": "EQ",
                        "arguments": {
                            "field": "account",
                            "value": "account.name",
                            "custom": ""
                        }
                    },
                    {
                        "function": "EQ",
                        "arguments": {
                            "field": "username",
                            "value": "custom",
                            "custom": "true"
                        }
                    },
                    {
                        "function": "EQ",
                        "arguments": {
                            "field": "email",
                            "value": "custom",
                            "custom": "owner"
                        }
                    },
                    {
                        "function": "NOT_EQ",
                        "arguments": {
                            "field": "username",
                            "value": "custom",
                            "custom": "owner"
                        }
                    },
                    {
                        "function": "START",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "jj"
                        }
                    },
                    {
                        "function": "NOT_START",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "mi"
                        }
                    },
                    {
                        "function": "END",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "jj"
                        }
                    },
                    {
                        "function": "NOT_END",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "ke"
                        }
                    },
                    {
                        "function": "CONTAIN",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "jj"
                        }
                    },
                    {
                        "function": "NOT_CONTAIN",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "ik"
                        }
                    },
                    {
                        "function": "IN",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "jj"
                        }
                    },
                    {
                        "function": "NOT_IN",
                        "arguments": {
                            "field": "config.test",
                            "value": "custom",
                            "custom": "ik"
                        }
                    }
                ]
            }
        }
    })), "conditions", {
        "id": "12345",
        "username": "owner",
        "email": "mike@corsairm360.com",
        "account": "6041ed8e08acbf71381e0789",
        "primary": True,
        "config": {
            "test": "mike"
        }
    })
    assert not status

def test_can_access_conditions_fail_invalid_condition():
    status = rbac.can_access(build_request(to_json({
        "user": {
            "id": "12345",
            "username": "owner",
            "email": "mike@corsairm360.com",
            "account": {
                "_id": "6041ed8e08acbf71381e0789",
                "name": "mikeorg",
            }
        },
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "conditions": {
                "operator": "$and",
                "criteria": [
                    {
                        "function": "Invalid",
                        "arguments": {
                            "field": "password",
                            "value": "password",
                            "custom": ""
                        }
                    }
                ]
            }
        }
    })), "condition", {
        "id": "12345",
        "username": "owner",
        "email": "mike@corsairm360.com",
        "account": "6041ed8e08acbf71381e0789",
        "primary": True,
        "config": {
            "test": "mike"
        }
    })
    assert not status

def test_can_access_conditions_fail_condition_parsing_error():
    status = rbac.can_access(build_request(to_json({
        "user": {
            "id": "12345",
            "username": "owner",
            "email": "mike@corsairm360.com",
            "account": {
                "_id": "6041ed8e08acbf71381e0789",
                "name": "mikeorg",
            }
        },
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "conditions": {
                "operator": "$and",
                "criteria": [
                    {
                        "function": "IN",
                        "arguments": {
                            "field": True,
                            "value": "test",
                            "custom": ""
                        }
                    }
                ]
            }
        }
    })), "conditions", {
        "id": "12345",
        "username": "owner",
        "email": "mike@corsairm360.com",
        "account": "6041ed8e08acbf71381e0789",
        "primary": True,
        "config": {
            "test": "mike"
        }
    })
    assert not status

def test_filter_fields_fail_invalid_data():
    data = {}
    status = rbac.filter_fields(build_request(to_json({
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "fields": {}
        }
    })), data)
    assert status == data

def test_filter_fields_success_no_rbac_configured():
    data = {"foo": "bar"}
    status = rbac.filter_fields(build_request(to_json({
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "fields": {
                "operator": None
            }
        }
    })), data)
    assert status == data

def test_filter_fields_success_will_work():
    data = {
        "_id": "1234",
        "username": "owner",
        "firstName": "owner",
        "lastName": "Maestro M360",
        "email": "mike@corsairm360.com",
        "status": "active",
        "profile": {},
        "ts": 1614693465902,
        "account": "45678",
        "groups": ["admin", "root"],
        "security": {"mfa": False},
        "tenants": [{"id": "abcd", "code": "M360"}],
        "config": {"M360": {"common": {"primary": True, "pet": "cersei", "foo": "bar"}, "specific": {}}},
        "auto_registration_flow": "corsair_saas"
    }
    status = rbac.filter_fields(build_request(to_json({
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "fields": {
                "operator": "allow",
                "list": {
                    "user": "username",
                    "email": "email",
                    "config": "config.M360.common"
                }
            }
        }
    })), data)
    assert status == {
        "_id": "1234",
        "username": "owner",
        "firstName": "owner",
        "lastName": "Maestro M360",
        "email": "mike@corsairm360.com",
        "status": "active",
        "profile": {},
        "ts": 1614693465902,
        "account": "45678",
        "groups": ["admin", "root"],
        "security": {"mfa": False},
        "tenants": [{"id": "abcd", "code": "M360"}],
        "config": {"M360": {"common": {"primary": True, "pet": "cersei", "foo": "bar"}}},
        "auto_registration_flow": "corsair_saas"
    }

def test_set_service_config_2():
    rbac.set_service_config({
        "contract": {
            "name": "express",
            "group": "Testing",
            "version": 1,
            "ports": {
                "data": 4002,
                "maintenance": 4002
            },
            "apis": {
                "main": {
                    "get": {
                        "/": {
                            "label": "get api",
                            "access": True
                        }
                    },
                    "post": {
                        "/": {
                            "access": False,
                            "label": "post api",
                            "rbac": {
                                "fields": ["config"]
                            }
                        }
                    }
                }
            }
        }
    })

def test_filter_fields_success_will_work_on_array_and_deny():
    data = [{
        "_id": "1234",
        "username": "owner",
        "firstName": "owner",
        "lastName": "Maestro M360",
        "email": "mike@corsairm360.com",
        "status": "active",
        "profile": {},
        "ts": 1614693465902,
        "account": "45678",
        "groups": ["admin", "root"],
        "security": {"mfa": False},
        "tenants": [{"id": "abcd", "code": "M360"}],
        "config": {"M360": {"common": {"primary": True, "pet": "cersei", "foo": "bar"}, "specific": {}}},
        "auto_registration_flow": "corsair_saas"
    }]
    status = rbac.filter_fields(build_request(to_json({
        "API": {
            "method": "get",
            "endpoint": "/"
        },
        "rbac": {
            "fields": {
                "operator": "deny",
                "list": {
                    "tenant": "tenants",
                    "security": "security",
                    "groups": "groups",
                    "config": "config.M360"
                }
            }
        }
    })), data)
    assert status == [
        {
            "_id": "1234",
            "username": "owner",
            "firstName": "owner",
            "lastName": "Maestro M360",
            "email": "mike@corsairm360.com",
            "status": "active",
            "profile": {},
            "ts": 1614693465902,
            "account": "45678",
            "groups": ["admin", "root"],
            "security": {"mfa": False},
            "tenants": [{"id": "abcd", "code": "M360"}],
            "config": {"M360": {"common": {"primary": True, "pet": "cersei", "foo": "bar"}, "specific": {}}},
            "auto_registration_flow": "corsair_saas"
        }
    ]
