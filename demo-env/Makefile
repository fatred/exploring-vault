# Cheater cheater makefile
#
.DEFAULT_GOAL := help

.PHONY: help deploy destroy 

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

## deploy shortcuts

deploy:
	sudo clab deploy -c
	cp clab-demo-env/ansible-inventory.yml ansible-inventory.yml
	sudo sed -i -E 's/([[:space:]]+)(clab-demo-env-[^[:space:]]+)/\1\2 \2.problemofnetwork.com/' /etc/hosts
#	sed -i '/linux:/!b;n;s/vars:/vars: {}/' ansible-inventory.yml

preflight-checks:
	python3 test-inventory.py
	python3 query_gnmi_cert.py clab-demo-env-spine1
	python3 query_gnmi_cert.py clab-demo-env-leaf1
	python3 query_gnmi_cert.py clab-demo-env-leaf2
	openssl s_client -showcerts -connect clab-demo-env-leaf1:443 2>/dev/null </dev/null | grep "Server certificate" -A2 && echo ""
	openssl s_client -showcerts -connect clab-demo-env-leaf2:443 2>/dev/null </dev/null | grep "Server certificate" -A2 && echo ""
	openssl s_client -showcerts -connect clab-demo-env-spine1:443 2>/dev/null </dev/null | grep "Server certificate" -A2 && echo ""

preflight-tests:
	python3 test-pygnmi-clab.py
	python3 test-jsonrpc-clab.py

trust:
	sudo cp ../terraform/root_ca_g1.crt /usr/local/share/ca-certificates/
	sudo cp ../terraform/pon_issuing_g1.crt /usr/local/share/ca-certificates/
	sudo update-ca-certificates

issue-certs:
	python3 issue_device_certs_nornir.py

push-tls-profile:
	python3 push_tls_profile_nornir.py
	echo "waiting for jsonrpc to restart" && sleep 5
	python3 apply_gnmi_tls_profile_jsonrpc.py

destroy:
	sudo clab destroy -c
	rm ansible-inventory.yml

postflight-checks:
	openssl s_client -showcerts -connect clab-demo-env-leaf1.problemofnetwork.com:443 2>/dev/null </dev/null | grep "Server certificate" -A2 && echo ""
	openssl s_client -showcerts -connect clab-demo-env-leaf2.problemofnetwork.com:443 2>/dev/null </dev/null | grep "Server certificate" -A2 && echo ""
	openssl s_client -showcerts -connect clab-demo-env-spine1.problemofnetwork.com:443 2>/dev/null </dev/null | grep "Server certificate" -A2 && echo ""
	python3 query_gnmi_cert.py clab-demo-env-spine1.problemofnetwork.com
	python3 query_gnmi_cert.py clab-demo-env-leaf1.problemofnetwork.com
	python3 query_gnmi_cert.py clab-demo-env-leaf2.problemofnetwork.com

postflight-tests:
	python3 test-pygnmi-vault.py
	python3 test-jsonrpc-vault.py
