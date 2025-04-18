#!/usr/bin/env python3
from rich import print
from pygnmi.client import gNMIclient
from models import nokia, business


def _build_aaa_role_item(
    rolename: str, roletype: business.AaaRoleTypes
) -> nokia.AaaRoleItem:
    aaa_roleitem = nokia.AaaRoleItem(
        rolename=rolename,
        services=roletype,
    )
    return aaa_roleitem


def _build_aaa_user_item(
    username: str, pwdhash: str, role: str, ssh_key: str
) -> nokia.UserItem:
    return nokia.UserItem(
        username=username,
        password=pwdhash,
        role=[role],
        ssh_key=[ssh_key],
    )


def _build_nokia_aaa_users_model(userlist: list) -> nokia.Model:
    return nokia.Model(
        system=nokia.System(
            aaa=nokia.Aaa(authentication=nokia.Authentication(user=userlist))
        )
    )


def _build_nokia_aaa_group_model(aaarolelist: list) -> nokia.Model:
    return nokia.Model(
        system=nokia.System(
            aaa=nokia.Aaa(authorization=nokia.Authorization(role=aaarolelist))
        )
    )


def _build_nokia_sys_role_model(sysrolelist: list) -> nokia.Model:
    return nokia.Model(
        system=nokia.System(configuration=nokia.Configuration(role=sysrolelist))
    )


# groups
global_write = nokia.PathRuleItem(
    path_reference="/", action=nokia.PathRuleActions.write
)
global_read = nokia.PathRuleItem(path_reference="/", action=nokia.PathRuleActions.read)
backup_read = nokia.PathRuleItem(path_reference="/", action=nokia.PathRuleActions.read)

# build sysgroups
sys_netadmin = nokia.SysRoleItem(name="netadmin", rule=[global_write])


# build user
jhoward_user = _build_aaa_user_item(
    username="jhoward",
    pwdhash="$ar2$X0t/iUPPOgY=$0OqEK68HOWPQXDe81uQ6Vw==",
    role="netadmin",
    ssh_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC0e1FGLpTw4egTHzXWjRIjyL6BmZhIkE/Kwdo2Fe7wAA4MN7GBj2s/dXFQNYynI4ZyU6vIrkMXUtVjucMUy3Wft3WP5DPrmLVPlHjBmcBJgUuGlzGGiTUqPojrstUNSiT92plqEoYTttQjtaNQfMSj1OH9bp1MT9AX8V4f8nGW4nHEbge24Qwyq0KyY0hTkhJlfLoeqMqXTuVF/xJ9qE67p/odTB9DQiFeWsG1KJs6EJdaFnbnPB4E2UMw/LTry2uavgbaZX+vtORMeebXU8EUFh+ZeigFaziq1fedc1GGgwIEKLs3fQ13yT3Rr19Kgr0g0nG8u4d24tQdtBnC/E1P",
)
# build role
role_netadmin = _build_aaa_role_item(
    rolename="netadmin", roletype=business.AaaRoleTypes.human_admin
)

# create final objects
aaa_users = _build_nokia_aaa_users_model([jhoward_user])
aaa_groups = _build_nokia_aaa_group_model([role_netadmin])
sys_roles = _build_nokia_sys_role_model([sys_netadmin])

print(aaa_groups.model_dump_json(exclude_unset=True, by_alias=True))
print(sys_roles.model_dump_json(exclude_unset=True, by_alias=True))
print(aaa_users.model_dump_json(exclude_unset=True, by_alias=True))

# host = ("clab-demo-env-spine1", "57400")
# set_config = [
#     ("/", aaa_groups.model_dump_json(exclude_unset=True, by_alias=True)),
#     ("/", sys_roles.model_dump_json(exclude_unset=True, by_alias=True)),
#     ("/", aaa_users.model_dump_json(exclude_unset=True, by_alias=True)),
# ]

# if __name__ == "__main__":
#     with gNMIclient(
#         target=host,
#         username="admin",
#         password="NokiaSrl1!",
#         path_root="clab-demo-env/.tls/ca/ca.pem",
#     ) as gc:
#         result = gc.set(update=set_config)
#         print(result)
