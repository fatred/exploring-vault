#!/usr/bin/env python3
import requests
import json

TLS_PROFILE_NAME = "vault-profile"

device_list = [
    "clab-demo-env-leaf1.problemofnetwork.com",
    "clab-demo-env-leaf2.problemofnetwork.com",
    "clab-demo-env-spine1.problemofnetwork.com",
]
jsonrpc_path = "/jsonrpc"
default_cred = ("admin", "NokiaSrl1!")
headers = {"Content-type": "application/json"}


def build_rpc_request(path: str, value: dict) -> str:
    body = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "set",
        "params": {"commands": [{"action": "update", "path": path, "value": value}]},
    }
    return body


for device in device_list:
    url = f"https://{device}{jsonrpc_path}"
    gnmi_update_req = requests.post(
        url,
        data=json.dumps(build_rpc_request("/system/gnmi-server/network-instance[name=mgmt]", {"tls-profile": f"{TLS_PROFILE_NAME}"})),
        headers=headers,
        auth=requests.auth.HTTPBasicAuth(*default_cred),
        verify=True,
    )

    print(f"{device}: status {gnmi_update_req.status_code} message {gnmi_update_req.json()['result'][0]}")
