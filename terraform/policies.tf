#-----------------------------------------
# Create a policy that can only read certs
#-----------------------------------------

resource "vault_policy" "pki-reader-vault-policy" {
  name = "pki-reader-vault-policy"

  policy = <<EOT
## place to store account details for automation towards the devices
path "network-automation/+/device-creds" {
  capabilities = ["read","list"]
}
path "network-automation/+/device-certs" {
  capabilities = ["read","list"]
}
## Vault TF provider requires ability to create a child token
path "auth/token/create" {  
  capabilities = ["create", "update", "sudo"]  
}
EOT
}

#----------------------------------------------
# Create a policy that can do anything to certs
#----------------------------------------------

resource "vault_policy" "pki-admin-vault-policy" {
  name = "pki-admin-vault-policy"

  policy = <<EOT
## place to store account details for automation towards the devices
path "network-automation/+/device-creds" {
  capabilities = ["create", "update"]
}
path "network-automation/+/device-creds" {
  capabilities = ["read","list"]
}
## place to store certificates we generate for the devices
path "network-automation/+/device-certs" {
  capabilities = ["create", "update"]
}
path "network-automation/+/device-certs" {
  capabilities = ["read","list"]
}
## Vault TF provider requires ability to create a child token
path "auth/token/create" {  
  capabilities = ["create", "update", "sudo"]  
}
EOT
}

###
# uncomment the below into the "pki-admin-vault-policy" between line 48/49
## Work with pki secrets engine
#path "pki*" {
#  capabilities = [ "create", "read", "update", "delete", "list", "sudo", "patch" ]
#}
###
