import hvac

PKI_MOUNT_POINT: str = "pki_int"
PKI_ROLE: str = "problemofnetwork-dot-com"
CERT_TTL: int = 86400
KV_MOUNT_POINT: str = "network-automation"
KV_PATH: str = "device-certs"


def generate_device_cert(client: hvac.Client, device_name: str, device_ip: str) -> dict:
    vault_cert = client.secrets.pki.generate_certificate(
        name=PKI_ROLE,
        common_name=device_name,
        extra_params={"ip_sans": device_ip, "ttl": CERT_TTL},
        mount_point=PKI_MOUNT_POINT,
    )
    return dict(vault_cert["data"])


def set_vault_device_cert(
    client: hvac.Client,
    kv_mount: str,
    kv_secret_name: str,
    device_name: str,
    cert_bundle: dict,
) -> (bool, int):
    results = client.secrets.kv.v2.patch(
        mount_point=kv_mount, path=kv_secret_name, secret={device_name: cert_bundle}
    )
    if results["warnings"] is None:
        return (True, results["data"]["version"])
    else:
        return (False, -1)


def get_vault_device_cert(
    client: hvac.Client, kv_mount: str, kv_secret_name: str, device_name: str
) -> dict:
    return client.secrets.kv.v2.read_secret_version(
        mount_point=kv_mount, path=kv_secret_name, raise_on_deleted_version=False
    )["data"]["data"][device_name]


if __name__ == "__main__":
    device_name: str = "leaf1.problemofnetwork.com"
    client = hvac.Client()
    test_cert = generate_device_cert(client, device_name, "172.20.20.3")
    print(
        f"Issued new cert for {device_name} with serial {test_cert['serial_number']} and expiry on {test_cert['expiration']}"
    )
    saved, secret_version = set_vault_device_cert(
        client, KV_MOUNT_POINT, KV_PATH, device_name, test_cert
    )
    if saved:
        print(
            f"Uploaded new cert for {device_name} to vault under {KV_MOUNT_POINT}/{KV_PATH}, stored with version {secret_version}"
        )
    else:
        print(
            f"Unable to upload cert to vault. Key material lost! Revoke {test_cert['serial_number']}"
        )
