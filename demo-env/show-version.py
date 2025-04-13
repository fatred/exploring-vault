from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_pygnmi.tasks import gnmi_get

nr = InitNornir(config_file="config.yaml")

srl = nr.filter(F(groups__contains="nokia_srlinux"))

result1 = srl.run(task=gnmi_get, encoding="json_ietf", path=["system/information/version"])
print_result(result1)
