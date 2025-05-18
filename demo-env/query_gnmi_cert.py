#!/usr/bin/env python3
import ssl
import socket
import argparse
from cryptography import x509
from cryptography.hazmat.backends import default_backend


def get_server_cert_cn_issuer(hostname, port) -> tuple:
    # Create a socket and wrap it in SSL without verification
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # Do NOT verify the cert

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            der_cert = ssock.getpeercert(binary_form=True)
            cert = x509.load_der_x509_certificate(der_cert, default_backend())

            # Extract CN (Common Name) from subject
            subject = cert.subject
            cn = subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value

            # Extract Issuer
            issuer = cert.issuer.rfc4514_string()

            return (cn, issuer)


def main(args):
    cn, issuer = get_server_cert_cn_issuer(args.hostname, args.port)
    print(f"CN: {cn}")
    print(f"Issuer: {issuer}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch CN and Issuer from gNMI server certificate")
    parser.add_argument("hostname", type=str, help="Hostname or IP of gNMI server")
    parser.add_argument("-p", "--port", type=int, default=57400, help="Port number (default: 57400)")

    args = parser.parse_args()
    main(args)
