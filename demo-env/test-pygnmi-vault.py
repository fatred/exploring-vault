# Modules
from pygnmi.client import gNMIclient
import json

# Variables
port = 57400
hosts = ['clab-demo-env-leaf1.problemofnetwork.com', 'clab-demo-env-leaf2.problemofnetwork.com', 'clab-demo-env-spine1.problemofnetwork.com']

# Body
if __name__ == '__main__':
    for host in hosts:
        with gNMIclient(target=(host, port), username='admin', password='NokiaSrl1!') as gc:
             result = gc.get(path=['system/name'])

        print(f"connected with system certs via gnmi to {json.dumps(result['notification'][0]['update'][0]['val'])}")
