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

#--------------------------------------------------
# Create a policy that everyone can read user-creds
#--------------------------------------------------

resource "vault_policy" "user-creds-global-read-vault-policy" {
  name = "user-creds-read-vault-policy"

  policy = <<EOT
## place to store personal account details for user profile management on estate
path "user-creds/+" {
  capabilities = ["read","list"]
}
EOT
}

#---------------------------------------------------------------
# Create a user policy that enables personal write of user-creds
#---------------------------------------------------------------

resource "vault_policy" "user-creds-jhow-write-vault-policy" {
  name = "user-creds-jhow-write-vault-policy"

  policy = <<EOT
## place to store personal account details for user profile management on estate
path "user-creds/+/jhow" {
  capabilities = [ "create", "read", "update", "delete", "list", "sudo", "patch" ]
}
EOT
}

resource "vault_policy" "user-creds-ubaumann-write-vault-policy" {
  name = "user-creds-ubaumann-write-vault-policy"

  policy = <<EOT
## place to store personal account details for user profile management on estate
path "user-creds/+/ubaumann" {
  capabilities = [ "create", "read", "update", "delete", "list", "sudo", "patch" ]
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
