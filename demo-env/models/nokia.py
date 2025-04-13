#!/usr/bin/env python3
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


## enums
class AaaServices(str, Enum):
    cli = "cli"
    gnmi = "gnmi"
    jsonrpc = "json-rpc"


class PathRuleActions(str, Enum):
    deny = "deny"
    read = "read"
    write = "write"


# System Role
class PathRuleItem(BaseModel):
    path_reference: str = Field(serialization_alias="path-reference")
    action: str


class SysRoleItem(BaseModel):
    name: str
    rule: List[PathRuleItem]


class Configuration(BaseModel):
    role: List[SysRoleItem]


## AAA Group
class AaaRoleItem(BaseModel):
    rolename: str
    services: List[str]


class Authorization(BaseModel):
    role: List[AaaRoleItem]


## AAA User
class UserItem(BaseModel):
    username: str
    password: str
    role: List[str]
    ssh_key: List[str] = Field(serialization_alias="ssh-key")


class Authentication(BaseModel):
    user: List[UserItem]

## AAA Common
class Aaa(BaseModel):
    authentication: Optional[Authentication] = None
    authorization: Optional[Authorization] = None


class System(BaseModel):
    aaa: Optional[Aaa] = None
    configuration: Optional[Configuration] = None


class Model(BaseModel):
    system: System
