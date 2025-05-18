# Modules
from pygnmi.client import gNMIclient
import json

# Variables
port = 57400
hosts = ['clab-demo-env-spine1', 'clab-demo-env-leaf1', 'clab-demo-env-leaf2']

# Body
if __name__ == '__main__':
    for host in hosts:
        #with gNMIclient(target=(host, port), username='admin', password='NokiaSrl1!', path_cert="clab-demo-env/.tls/ca/ca.pem") as gc:
        with gNMIclient(target=(host, port), username='admin', password='NokiaSrl1!', verify=False) as gc:
             result = gc.get(path=['system/name'])    
        print(f"connected with clab certs on gnmi to {json.dumps(result['notification'][0]['update'][0]['val'])}")
