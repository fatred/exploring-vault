#!/usr/bin/env python3
import requests
import json

device_list = [
    "clab-demo-env-leaf1",
    "clab-demo-env-leaf2",
    "clab-demo-env-spine1",
]
jsonrpc_path = "/jsonrpc"
default_cred = ("admin", "NokiaSrl1!")
headers = {"Content-type": "application/json"}


def build_rpc_request(path: str, datastore: str) -> str:
    body = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "get",
        "params": {"commands": [{"path": path, "datastore": datastore}]},
    }
    return body


for device in device_list:
    url = f"https://{device}{jsonrpc_path}"
    gnmi_update_req = requests.post(
        url,
        data=json.dumps(build_rpc_request("/system/name", "state")),
        headers=headers,
        auth=requests.auth.HTTPBasicAuth(*default_cred),
        verify=False,
    )

    print(f"{device}: status {gnmi_update_req.status_code} message {gnmi_update_req.json()['result'][0]}")
