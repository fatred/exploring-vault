from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_pygnmi.tasks import gnmi_set
from nornir.core.task import Task, Result
from nornir.core.filter import F
import hvac

DN: str = "problemofnetwork.com"
KV_MOUNT_POINT: str = "network-automation"
KV_PATH: str = "device-certs"
TLS_PROFILE_NAME = "vault-profile"


def _get_vault_device_cert(
    client: hvac.Client, kv_mount: str, kv_secret_name: str, device_name: str
) -> dict:
    return client.secrets.kv.v2.read_secret_version(
        mount_point=kv_mount, path=kv_secret_name, raise_on_deleted_version=False
    )["data"]["data"][device_name]


def push_tls_profile(task: Task) -> Result:
    client = hvac.Client()
    fqdn = f"{task.host.name}.{DN}"
    key_material = _get_vault_device_cert(client=client, kv_mount=KV_MOUNT_POINT, kv_secret_name=KV_PATH, device_name=fqdn)
    set_config = [
        (
            "system", {
                "tls": {
                    "server-profile": [
                        {
                            "name": f"{TLS_PROFILE_NAME}",
                            "key": f"{key_material['private_key']}",
                            "certificate": f"{key_material['certificate']}",
                            "authenticate-client": False
                        }
                    ]
                }
            }
        )
    ]
    # bit of a hack
    me = nr.filter(F(name__eq=task.host.name))
    push_profile = me.run(task=gnmi_set, encoding="json_ietf", update=set_config)
    if push_profile[task.host.name].failed:
        result_msg: str = f"UPDATE to {task.host.name} failed"
        success = False
    elif push_profile[task.host.name].changed:
        result_msg: str = f"UPDATE to {task.host.name} was successful"
        success = True
    else:
        result_msg: str = f"UPDATE to {task.host.name} was unnecessary"
        success = True
    return Result(host=task.host, result=result_msg, changed=success)


def set_jsonrpc_tls_profile(profile_name: str) -> list:
    return [
        (
            "system", {
                "json-rpc-server": {
                    "network-instance": [
                        {
                            "name": "mgmt",
                            "https": {
                                "tls-profile": f"{profile_name}"
                            }
                        }
                    ]
                }
            }
        )
    ]


if __name__ == '__main__':
    nr = InitNornir(config_file="config.yaml")
    push_tls_profile = nr.run(task=push_tls_profile)
    print_result(push_tls_profile)
    apply_jsonrpc_tls_profile = nr.run(task=gnmi_set, encoding="json_ietf", update=set_jsonrpc_tls_profile(TLS_PROFILE_NAME))
    print_result(apply_jsonrpc_tls_profile)
