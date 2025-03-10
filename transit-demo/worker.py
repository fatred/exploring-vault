#!/usr/bin/env python3
"""
Author: John Howard <fatred@gmail.com>

Simple script that emulates a worker process communicating with NATS sending 
messages on a sender queue to be consumed by another worker, who will return 
them back on a reply queue. Use command line args to establish if we are 
sender or reciever.
"""
import asyncio
import argparse
import nats


## CONSTANTS
# connstring to the NATS server
NATS_SERVER_CONNSTRING: str = "nats://localhost:4222"
# names are from the perspective of the emitting worker.
NATS_TX_QUEUE: str = "transit-demo-transmit"
NATS_RX_QUEUE: str = "transit-demo-recieve"


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


async def main(role: str):
    # connect to NATS server.
    nc = await nats.connect(NATS_SERVER_CONNSTRING)

    # subscribe to the correct queue for recieving messages async in role.
    print(f"Subscribing to {pick_subscription_queue(role)}")
    sub = await nc.subscribe(pick_subscription_queue(role))

    # if outbound worker, send a message to the TX queue, wait for reply
    #   before ending async.
    if role == "initiator":
        await nc.publish(pick_transmit_queue(role), b"this is an emitted message")

    # handle a message on our queue
    try:
        async for msg in sub.messages:
            # extract the message attributes once
            queue = msg.subject
            content = msg.data.decode()
            if role == "observer":
                # we are the responder, and we just got a message from the initator
                # announce message content
                print(f"Received a message on '{queue}': {content}")
            elif role == "responder":
                # we are the responder, and we just got a message from the initator
                # announce message content
                print(f"Received a message on '{queue}': {content}")
                # announce the reply and queue
                print(f"Parroting it back to {pick_transmit_queue(role)}")
                # encode our response to bytes
                reply = bytes(f"i saw {content}", 'utf-8')
                # push message 
                await nc.publish(pick_transmit_queue(role), reply)
                # we only want one so time to cleanup
                await sub.unsubscribe()
            else: 
                # we are the initiator, waiting for the parrot response.
                print(f"Received parroted message on '{queue}': {content}")
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
    role_group = parser.add_mutually_exclusive_group(required=True)
    role_group.add_argument('--initiator', action='store_true')
    role_group.add_argument('--responder', action='store_true')
    role_group.add_argument('--observer', action='store_true')
    args = parser.parse_args()
    if args.responder:
        role = "responder"
    elif args.observer:
        role = "observer"
    else:
        role = "initiator"

    # call main.
    asyncio.run(main(role))
