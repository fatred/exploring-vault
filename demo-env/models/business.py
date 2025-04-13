#!/usr/bin/env python3
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from models import nokia


## enums
class AaaRoleTypes(list, Enum):
    human_admin = [nokia.AaaServices.cli, nokia.AaaServices.gnmi, nokia.AaaServices.jsonrpc]
    human_guest = [nokia.AaaServices.cli, nokia.AaaServices.gnmi, nokia.AaaServices.jsonrpc]
    workflow_read = [nokia.AaaServices.gnmi, nokia.AaaServices.jsonrpc]
    workflow_write = [nokia.AaaServices.gnmi, nokia.AaaServices.jsonrpc]
    backup = [nokia.AaaServices.cli]


#class PathRules(list, Enum):
#    global_write = [path_reference=, action=nokia.PathRuleActions.write]
#    global_read = [path_reference="/", action=nokia.PathRuleActions.read]
#    backup_read = [path_reference="/", action=nokia.PathRuleActions.read]
#
#
#class PathRuleMapping(list, Enum):
#    human_admin = [PathRules.global_write]
#    human_guest = [PathRules.global_read]
#    backup = [PathRules.backup_read]


#class AaaServices(str, Enum):
#    cli = "cli"
#    gnmi = "gnmi"
#    jsonrpc = "json-rpc"
#
#
#class PathRuleActions(str, Enum):
#    deny = "deny"
#    read = "read"
#    write = "write"
#
#
## System Role
#class PathRuleItem(BaseModel):
#    path_reference: str = Field(serialization_alias="path-reference")
#    action: str

