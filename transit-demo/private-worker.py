#!/usr/bin/env python3
"""
Author: John Howard <fatred@gmail.com>

Simple script that emulates a worker process communicating with NATS sending 
messages on a sender queue to be consumed by another worker, who will return 
them back on a reply queue. Use command line args to establish if we are 
sender or reciever. Encrypt all the data in transit.
"""
import asyncio
import argparse
import nats
import hvac
import base64


## CONSTANTS
# NATS stuff
# connstring to the NATS server
NATS_SERVER_CONNSTRING: str = "nats://localhost:4222"
# names are from the perspective of the emitting worker.
NATS_TX_QUEUE: str = "transit-demo-transmit"
NATS_RX_QUEUE: str = "transit-demo-recieve"
# Vault stuff
VAULT_USER1: str = "nats-worker1"
VAULT_USER2: str = "nats-worker2"
VAULT_PASS: str = "Less-Secure-Cred!"
TRANSIT_MOUNT: str = "transit-nats"
TRANSIT_KEY: str = "demo_key"


def pick_subscription_queue(role: str) -> str:
    """Take the role name and reply the name of the queue to subscribe to.
    Subscriptions are "inbound" to that worker

    Responders should be subscribed to the TX queue.
    Initiators should be subscribed to the RX queue.

    Args:
        role (str): role from argparse.

    Returns:
        str: queuename to subscribe to.
    """
    return NATS_RX_QUEUE if role == "initiator" else NATS_TX_QUEUE


def pick_transmit_queue(role: str) -> str:
    """Take the role name and reply the name of the queue to transmit on.
    Transmissions are "outbound" to that worker

    Initiators should be emitting to the TX queue.
    Responders should be emitting to the RX queue.

    Args:
        role (str): role from argparse.

    Returns:
        str: queuename to transmit to.
    """
    return NATS_TX_QUEUE if role == "initiator" else NATS_RX_QUEUE


def encrypt_string(input: str, client: hvac.Client) -> str:
    encrypt_data_response = client.secrets.transit.encrypt_data(name=TRANSIT_KEY, mount_point = TRANSIT_MOUNT, plaintext = base64.b64encode(input.encode()).decode())
    ciphertext = encrypt_data_response['data']['ciphertext']
    return ciphertext


def decrypt_string(input: str, client: hvac.Client) -> str:
    decrypt_data_response = client.secrets.transit.decrypt_data(name=TRANSIT_KEY, mount_point = TRANSIT_MOUNT, ciphertext = input)
    plaintext = base64.b64decode(decrypt_data_response['data']['plaintext']).decode()
    return plaintext


def auth_vault(user: int) -> hvac.Client:
    # setup vault client
    client = hvac.Client()
    # auth with userpass
    if user == 1:
        client.auth.userpass.login(username=VAULT_USER1, password=VAULT_PASS)
    elif user == 2:
        client.auth.userpass.login(username=VAULT_USER2, password=VAULT_PASS)
    else:
        # assume we have a token in env
        client.auth.login()
    # if it didnt work, quit.
    if not client.is_authenticated():
        print("Vault auth failed!")
        exit
    # we have a valid session
    return client


async def main(role: str, message: str, user: int):
    # connect to vault with correct user
    client = auth_vault(user)
    
    # connect to NATS server.
    nc = await nats.connect(NATS_SERVER_CONNSTRING)

    # subscribe to the correct queue for recieving messages async in role.
    print(f"Subscribing to {pick_subscription_queue(role)}")
    sub = await nc.subscribe(pick_subscription_queue(role))

    # if outbound worker, send a message to the TX queue, wait for reply
    #   before ending async.
    if role == "initiator":
        await nc.publish(pick_transmit_queue(role), bytes(encrypt_string(message, client), 'utf-8'))

    # handle a message on our queue
    try:
        async for msg in sub.messages:
            # extract the message attributes once
            queue = msg.subject
            if role == "observer":
                content = msg.data.decode()
                # we are the responder, and we just got a message from the initator
                # announce message content
                print(f"Received a message on '{queue}': {content}")
            elif role == "responder":
                content = msg.data.decode()
                # we are the responder, and we just got a message from the initator
                # announce message content
                print(f"Received a message on '{queue}': {content}")
                plaintext = decrypt_string(input=content, client=client)
                print(f"I decrypted this and found plaintext: {plaintext}")
                # announce the reply and queue
                print(f"Acknowledging message back on {pick_transmit_queue(role)}")
                ack_message = f"Ack: {plaintext}"
                # encrupt our response
                crypted_ack_message = encrypt_string(ack_message, client=client)
                # encode our response to bytes
                reply = bytes(f"{crypted_ack_message}", 'utf-8')
                # push message 
                await nc.publish(pick_transmit_queue(role), reply)
                # we only want one so time to cleanup
                await sub.unsubscribe()
            else:
                content = msg.data.decode()
                # we are the initiator, waiting for the ack response.
                print(f"Received Ack message on '{queue}': {content}")
                plaintext = decrypt_string(input=content, client=client)
                print(f"Decrypted content: {plaintext}")
                # we only want one so time to cleanup
                await sub.unsubscribe()
    except Exception as e:
        # something broke - report what.
        print(e)

    # Terminate connection to NATS.
    await nc.drain()


if __name__ == "__main__":
    # parse args.
    #  options:
    #    role: initiator or responder.
    parser = argparse.ArgumentParser()
    parser.add_argument('--message', type=str, default="Empty Message")
    role_group = parser.add_mutually_exclusive_group(required=True)
    role_group.add_argument('--initiator', action='store_true')
    role_group.add_argument('--responder', action='store_true')
    role_group.add_argument('--observer', action='store_true')
    args = parser.parse_args()
    if args.responder:
        role = "responder"
        user = 2
    elif args.observer:
        role = "observer"
        user = 1
    else:
        role = "initiator"
        user = 1

    # call main.
    asyncio.run(main(role = role, message=args.message, user=user))
