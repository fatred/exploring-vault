#!/usr/bin/env python3
import hvac
import base64

# CONSTANTS
VAULT_USER: str = "nats-worker1"
VAULT_PASS: str = "Less-Secure-Cred!"
TRANSIT_MOUNT: str = "transit-nats"
TRANSIT_KEY: str = "demo_key"


def encrypt_string(input: str, client: hvac.Client) -> str:
    encrypt_data_response = client.secrets.transit.encrypt_data(name=TRANSIT_KEY, mount_point = TRANSIT_MOUNT, plaintext = base64.b64encode(input.encode()).decode())
    ciphertext = encrypt_data_response['data']['ciphertext']
    return ciphertext


def decrypt_string(input: str, client: hvac.Client) -> str:
    decrypt_data_response = client.secrets.transit.decrypt_data(name=TRANSIT_KEY, mount_point = TRANSIT_MOUNT, ciphertext = input)
    plaintext = base64.b64decode(decrypt_data_response['data']['plaintext']).decode()
    return plaintext


def main():
    # setup vault client
    client = hvac.Client()
    # auth with userpass
    client.auth.userpass.login(username=VAULT_USER, password=VAULT_PASS)
    # if it didnt work, quit.
    if not client.is_authenticated():
        print("Vault auth failed!")
        exit
    # we have a valid session
    # setup our "secret" and display it
    test_string: str = "this is private"
    print(f"Test string: {test_string}")

    encrypted_string: str = encrypt_string(input = test_string, client = client)
    print(f"Encrypted string: {encrypted_string}")
    decrypted_string: str = decrypt_string(input = encrypted_string, client = client)
    print(f"Decrypted string: {decrypted_string}")


if __name__ == "__main__":
    main()
