"""Ortelius Class Defintions and Reusable functions."""

import os
from datetime import datetime
import socket
from typing import Optional

import requests
from fastapi import HTTPException, Request, status
from pydantic import BaseModel


class StatusMsg(BaseModel):
    status: str
    service_name: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "status": "UP",
                "service_name": "ms-compver-crud"
            }
        }


class User(BaseModel):
    _key: str
    name: str
    domain_key: str
    domain: str
    email: Optional[str] = None
    phone: Optional[str] = None
    realname: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "admin",
                "domainid": 1,
                "domain": "GLOBAL",
                "email": "admin@ortelius.io",
                "phone": "505-444-5566",
                "realname": "Ortelius Admin"
            }
        }


class Group(BaseModel):
    _key: str
    name: str
    domain_key: str
    domain: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Administrators",
                "domainid": 1,
                "domain": "GLOBAL"
            }
        }


class Groups2Users(BaseModel):
    group_key: str
    user_key: str

    class Config:
        schema_extra = {
            "example": {
                "goupid": 1,
                "userid": 1
            }
        }


class GroupsForUser(BaseModel):
    groups: Optional[list[Group]] = None

    class Config:
        schema_extra = {
            "example": {
                "groups": [
                    {
                        "id": 1,
                        "name": "Administrators",
                        "domainid": 1,
                        "domain": "GLOBAL"
                    }
                ]
            }
        }


class UsersForGroup(BaseModel):
    users: Optional[list[User]] = None

    class Config:
        schema_extra = {
            "example": {
                "users": [
                    {
                        "id": 1,
                        "name": "admin",
                        "domainid": 1,
                        "domain": "GLOBAL",
                        "email": "admin@ortelius.io",
                        "phone": "505-444-5566",
                        "realname": "Ortelius Admin"
                    }
                ]
            }
        }


class AuditRecord(BaseModel):
    _key: str
    action: str
    user: User
    when: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "action": "Created",
                "user": {
                    "domainid": 1,
                    "domain": "GLOBAL",
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "when": '2023-04-23T10:20:30.400+02:30'
            }
        }


class Package(BaseModel):
    purl: str
    name: str
    version: str
    license_key: str
    license: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "purl": "pkg:deb/debian/libc-bin@2.19-18+deb8u7?arch=amd64&upstream=glibc&distro=debian-8",
                "name": "libc-bin",
                "version": "2.19.18+deb8u7",
                "licenseid": 23,
                "license": "GP-2.0"
            }
        }


class Readme(BaseModel):
    _key: str
    content: list[str]

    class Config:
        schema_extra = {
            "example": {
                "id": 2344,
                "content": [
                    "# README",
                    "## Sample"
                ]
            }
        }


class License(BaseModel):
    _key: str
    content: list[str]

    class Config:
        schema_extra = {
            "example": {
                "id": 1244,
                "content": [
                    "# Apache 2",
                    "## Summary"
                ]
            }
        }


class Swagger(BaseModel):
    _key: str
    content: list[str]

    class Config:
        schema_extra = {
            "example": {
                "id": 334,
                "content": [
                    "# Rest APIs",
                    "## GET /user"
                ]
            }
        }


class Vulnerabilty(BaseModel):
    _key: str
    name: str

    class Config:
        schema_extra = {
            "example": {
                "id": 5534,
                "name": "CVE-1823"
            }
        }


class Providing(BaseModel):
    _key: str
    provides: list[str]

    class Config:
        schema_extra = {
            "example": {
                "id": 5987,
                "provides": [
                    "/user"
                ]
            }
        }


class Consuming(BaseModel):
    _key: str
    comsumes: list[str]

    class Config:
        schema_extra = {
            "example": {
                "id": 911,
                "consumes": [
                    "/user"
                ]
            }
        }


class ComponentVersion(BaseModel):
    _key: str
    name: str
    domain: str
    domain_key: str
    parent: Optional[str] = None
    parentid: Optional[int] = None
    predecessor: Optional[str] = None
    predecessorid: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 911,
                "name": "Hello World;v1.0.0",
                "domain": "GLOBAL.My Project",
                "domainid": 200,
                "parent": None,
                "parentid": None,
                "predecessor": None,
                "predecessorid": None
            }
        }


class ApplicationVersion(BaseModel):
    _key: str
    name: str
    domain: str
    domain_key: str
    parent: Optional[str] = None
    parentid: Optional[int] = None
    predecessor: Optional[str] = None
    predecessorid: Optional[int] = None
    deployments: Optional[list[int]] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 554,
                "name": "Hello App;v1",
                "domain": "GLOBAL.My Project",
                "domainid": 234,
                "parent": None,
                "parentid": None,
                "predecessor": None,
                "predecessorid": None,
                "deployments": [
                    121
                ]
            }
        }


class CompAttrs(BaseModel):
    builddate: Optional[str] = None
    buildid: Optional[str] = None
    buildurl: Optional[str] = None
    chart: Optional[str] = None
    chartnamespace: Optional[str] = None
    chartrepo: Optional[str] = None
    chartrepourl: Optional[str] = None
    chartversion: Optional[str] = None
    discordchannel: Optional[str] = None
    dockerrepo: Optional[str] = None
    dockersha: Optional[str] = None
    dockertag: Optional[str] = None
    gitcommit: Optional[str] = None
    gitrepo: Optional[str] = None
    gittag: Optional[str] = None
    giturl: Optional[str] = None
    hipchatchannel: Optional[str] = None
    pagerdutybusinessurl: Optional[str] = None
    pagerdutyurl: Optional[str] = None
    repository: Optional[str] = None
    serviceowner: Optional[User] = None
    slackchannel: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "builddate": "Mon Jan 31 16:18:26 2022",
                "buildid": "178",
                "buildurl": "https://circleci.com/gh/ortelius/store-cartservice/178",
                "chart": "chart/ms-cartservice",
                "chartnamespace": "default",
                "chartrepo": "msproject/ms-chartservice",
                "chartrepourl": "https://helm.msprogject/stable/msproject/ms-chartservice",
                "chartversion": "1.0.0",
                "discordchannel": "https://discord.gg/A4hx3",
                "dockerrepo": "myproject/ms-chartservice",
                "dockersha": "5d3d677e1",
                "dockertag": "v1.0.0",
                "gitcommit": "2adc111",
                "gitrepo": "msproject/ms-chartservice",
                "gittag": "main",
                "giturl": "https://github.com/msproject/ms-chartservice",
                "hipchatchannel": "",
                "pagerdutybusinessurl": "https://pagerduty.com/business/ms-chartservice",
                "pagerdutyurl": "https://pagerduty.com/business/ms-chartservice",
                "serviceowner": {
                    "id": 1,
                    "name": "admin",
                    "domainid": 1,
                    "domain": "GLOBAL",
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "slackchannel": "https://myproject.slack.com/444aaa"
            }
        }


class ComponentVersionDetails(ComponentVersion):
    owner: User
    creator: User
    created: datetime
    comptype: str
    packages: Optional[list[Package]] = None
    vulnerabilties: Optional[list[Vulnerabilty]] = None
    readme: Optional[Readme] = None
    license: Optional[License] = None
    swagger: Optional[Swagger] = None
    applications: Optional[list[ApplicationVersion]] = None
    providing: Optional[Providing] = None
    consuming: Optional[Consuming] = None
    attrs: Optional[CompAttrs] = None
    auditlog: Optional[list[AuditRecord]] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 911,
                "name": "Hello World;v1.0.0",
                "domain": "GLOBAL.My Project",
                "domainid": 200,
                "parent": None,
                "parentid": None,
                "predecessor": None,
                "predecessorid": None,
                "owner": {
                    "id": 1,
                    "name": "admin",
                    "domainid": 1,
                    "domain": "GLOBAL",
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "creator": {
                    "id": 1,
                    "name": "admin",
                    "domainid": 1,
                    "domain": "GLOBAL",
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "created": '2023-04-23T10:20:30.400+02:30',
                "comptype": "docker",
                "packages": [
                    {
                        "purl": "pkg:deb/debian/libc-bin@2.19-18+deb8u7?arch=amd64&upstream=glibc&distro=debian-8",
                        "name": "libc-bin",
                        "version": "2.19.18+deb8u7",
                        "licenseid": 23,
                        "license": "GP-2.0"
                    }
                ],
                "vulnerabilties": [
                    {
                        "id": 5534,
                        "name": "CVE-1823"
                    }
                ],
                "readme": {
                    "id": 2344,
                    "content": [
                        "# README",
                        "## Sample"
                    ]
                },
                "license": {
                    "id": 1244,
                    "content": [
                        "# Apache 2",
                        "## Summary"
                    ]
                },
                "swagger": {
                    "id": 334,
                    "content": [
                        "# Rest APIs",
                        "## GET /user"
                    ]
                },
                "applications": [

                ],
                "providing": {
                    "id": 5987,
                    "provides": [
                        "/user"
                    ]
                },
                "consuming": {
                    "id": 911,
                    "consumes": [
                        "/user"
                    ]
                },
                "attrs": {
                    "builddate": "Mon Jan 31 16:18:26 2022",
                    "buildid": "178",
                    "buildurl": "https://circleci.com/gh/ortelius/store-cartservice/178",
                    "chart": "chart/ms-cartservice",
                    "chartnamespace": "default",
                    "chartrepo": "msproject/ms-chartservice",
                    "chartrepourl": "https://helm.msprogject/stable/msproject/ms-chartservice",
                    "chartversion": "1.0.0",
                    "discordchannel": "https://discord.gg/A4hx3",
                    "dockerrepo": "myproject/ms-chartservice",
                    "dockersha": "5d3d677e1",
                    "dockertag": "v1.0.0",
                    "gitcommit": "2adc111",
                    "gitrepo": "msproject/ms-chartservice",
                    "gittag": "main",
                    "giturl": "https://github.com/msproject/ms-chartservice",
                    "hipchatchannel": "",
                    "pagerdutybusinessurl": "https://pagerduty.com/business/ms-chartservice",
                    "pagerdutyurl": "https://pagerduty.com/business/ms-chartservice",
                    "serviceowner": "stella99",
                    "serviceowneremail": "stella99@gmail.com",
                    "serviceownerid": "345",
                    "serviceownerphone": "505-444-5566",
                    "slackchannel": "https://myproject.slack.com/444aaa"
                }
            }
        }


class ApplicationVersionDetails(ApplicationVersion):
    owner: User
    creator: User
    created: datetime
    components: Optional[list[ComponentVersion]] = None
    auditlog: Optional[list[AuditRecord]] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 554,
                "name": "Hello App;v1",
                "domain": "GLOBAL.My Project",
                "domainid": 234,
                "parent": None,
                "parentid": None,
                "predecessor": None,
                "predecessorid": None,
                "deployments": None,
                "owner": {
                    "id": 1,
                    "name": "admin",
                    "domainid": 1,
                    "domain": "GLOBAL",
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "creator": {
                    "id": 1,
                    "name": "admin",
                    "domainid": 1,
                    "domain": "GLOBAL",
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "created": '2023-04-23T10:20:30.400+02:30',
                "components": [
                    {
                        "id": 911,
                        "name": "Hello World;v1.0.0",
                        "domain": "GLOBAL.My Project",
                        "domainid": 200,
                        "parent": None,
                        "parentid": None,
                        "predecessor": None,
                        "predecessorid": None
                    }
                ],
                "auditlog": None
            }
        }


class Environment(BaseModel):
    _key: str
    name: str
    domain: str
    domain_key: str
    owner: User
    creator: User
    created: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 911,
                "name": "Hello World;v1.0.0",
                "domain": "GLOBAL.My Project",
                "domainid": 200,
                "owner": {
                    "id": 1,
                    "name": "admin",
                    "domainid": 1,
                    "domain": "GLOBAL",
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "creator": {
                    "id": 1,
                    "name": "admin",
                    "domainid": 1,
                    "domain": "GLOBAL",
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "created": '2023-04-23T10:20:30.400+02:30'
            }
        }


class Deployment(BaseModel):
    _key: str
    environment: Environment
    application: ApplicationVersion
    components: list[ComponentVersion]
    starttime: datetime
    endtime: Optional[datetime] = None
    result: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "environment": {
                    "id": 911,
                    "name": "Hello World;v1.0.0",
                    "domain": "GLOBAL.My Project",
                    "domainid": 200,
                    "owner": {
                        "id": 1,
                        "name": "admin",
                        "domainid": 1,
                        "domain": "GLOBAL",
                        "email": "admin@ortelius.io",
                        "phone": "505-444-5566",
                        "realname": "Ortelius Admin"
                    },
                    "creator": {
                        "id": 1,
                        "name": "admin",
                        "domainid": 1,
                        "domain": "GLOBAL",
                        "email": "admin@ortelius.io",
                        "phone": "505-444-5566",
                        "realname": "Ortelius Admin"
                    },
                    "created": '2023-04-23T10:20:30.400+02:30'
                },
                "application": {
                    "id": 554,
                    "name": "Hello App;v1",
                    "domain": "GLOBAL.My Project",
                    "domainid": 234,
                    "parent": None,
                    "parentid": None,
                    "predecessor": None,
                    "predecessorid": None,
                    "deployments": None
                },
                "components": [
                    {
                        "id": 911,
                        "name": "Hello World;v1.0.0",
                        "domain": "GLOBAL.My Project",
                        "domainid": 200,
                        "parent": None,
                        "parentid": None,
                        "predecessor": None,
                        "predecessorid": None
                    }
                ],
                "starttime": '2023-04-23T10:20:30.400+02:30',
                "endtime": '2023-04-23T10:30:30.400+02:30',
                "result": 0
            }
        }


class DeploymentDetails(Deployment):
    log: Optional[list[str]] = None

    class Config:
        schema_extra = {
            "example": {
                "environment": {
                    "id": 911,
                    "name": "Hello World;v1.0.0",
                    "domain": "GLOBAL.My Project",
                    "domainid": 200,
                    "owner": {
                        "id": 1,
                        "name": "admin",
                        "domainid": 1,
                        "domain": "GLOBAL",
                        "email": "admin@ortelius.io",
                        "phone": "505-444-5566",
                        "realname": "Ortelius Admin"
                    },
                    "creator": {
                        "id": 1,
                        "name": "admin",
                        "domainid": 1,
                        "domain": "GLOBAL",
                        "email": "admin@ortelius.io",
                        "phone": "505-444-5566",
                        "realname": "Ortelius Admin"
                    },
                    "created": '2023-04-23T10:20:30.400+02:30'
                },
                "application": {
                    "id": 554,
                    "name": "Hello App;v1",
                    "domain": "GLOBAL.My Project",
                    "domainid": 234,
                    "parent": None,
                    "parentid": None,
                    "predecessor": None,
                    "predecessorid": None,
                    "deployments": None
                },
                "components": [
                    {
                        "id": 911,
                        "name": "Hello World;v1.0.0",
                        "domain": "GLOBAL.My Project",
                        "domainid": 200,
                        "parent": None,
                        "parentid": None,
                        "predecessor": None,
                        "predecessorid": None
                    }
                ],
                "starttime": '2023-04-23T10:20:30.400+02:30',
                "endtime": '2023-04-23T10:30:30.400+02:30',
                "result": 0
            },
            "log": [
                "Deploying Hello World",
                "Success"
            ]
        }


def validate_user(request: Request):
    try:
        validateuser_url = os.getenv('VALIDATEUSER_URL', None)

        if (validateuser_url is None):
            validateuser_host = os.getenv('MS_VALIDATE_USER_SERVICE_HOST', '127.0.0.1')
            host = socket.gethostbyaddr(validateuser_host)[0]
            validateuser_url = 'http://' + host + ':' + str(os.getenv('MS_VALIDATE_USER_SERVICE_PORT', 80))

        result = requests.get(validateuser_url + "/msapi/validateuser", cookies=request.cookies)
        if (result is None):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")

        if (result.status_code != status.HTTP_200_OK):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed status_code=" + str(result.status_code))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed:" + str(err)) from None
