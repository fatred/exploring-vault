from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Task, Result
import hvac

PKI_MOUNT_POINT: str = "pki_int"
PKI_ROLE: str = "problemofnetwork-dot-com"
DN: str = "problemofnetwork.com"
CERT_TTL: int = 86400
KV_MOUNT_POINT: str = "network-automation"
KV_PATH: str = "device-certs"


def _generate_device_cert(
    client: hvac.Client, device_name: str, device_ip: str
) -> dict:
    vault_cert = client.secrets.pki.generate_certificate(
        name=PKI_ROLE,
        common_name=device_name,
        extra_params={"ip_sans": device_ip, "ttl": CERT_TTL},
        mount_point=PKI_MOUNT_POINT,
    )
    return dict(vault_cert["data"])


def _set_vault_device_cert(
    client: hvac.Client,
    kv_mount: str,
    kv_secret_name: str,
    device_name: str,
    cert_bundle: dict,
) -> tuple[bool, int]:
    results = client.secrets.kv.v2.patch(
        mount_point=kv_mount, path=kv_secret_name, secret={device_name: cert_bundle}
    )
    if results["warnings"] is None:
        return (True, results["data"]["version"])
    else:
        return (False, -1)


def generate_cert_to_vault(task: Task) -> Result:
    client = hvac.Client()
    fqdn = f"{task.host.name}.{DN}"
    generated_keymat = _generate_device_cert(
        client=client, device_name=fqdn, device_ip=task.host.hostname
    )
    saved, secret_version = _set_vault_device_cert(
        client=client,
        kv_mount=KV_MOUNT_POINT,
        kv_secret_name=KV_PATH,
        device_name=fqdn,
        cert_bundle=generated_keymat,
    )
    if saved:
        result_msg: str = f"Uploaded new cert for {fqdn} to vault under {KV_MOUNT_POINT}/{KV_PATH}, stored with version {secret_version}"
        changed = True
    else:
        result_msg: str = f"Unable to upload cert to vault. Key material lost! Revoke {generated_keymat['serial_number']}"
        changed = False
    return Result(host=task.host, result=result_msg, changed=changed)


if __name__ == "__main__":
    nr = InitNornir(config_file="config.yaml")
    generate_certs_to_vault = nr.run(task=generate_cert_to_vault)
    print_result(generate_certs_to_vault)

