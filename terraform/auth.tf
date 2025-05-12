#--------------------------------
# Enable userpass auth method
#--------------------------------

resource "vault_auth_backend" "userpass" {
  type = "userpass"
}

#---------------------------------------------------------
# Create a user called pki-admin with a wonderful password
#---------------------------------------------------------

resource "vault_generic_endpoint" "pki-admin" {
  path                 = "auth/${vault_auth_backend.userpass.path}/users/pki-admin"
  ignore_absent_fields = true

  data_json = <<EOT
{
  "token_policies": ["pki-admin-vault-policy"],
  "password": "Velly-Secure-Cred!"
}
EOT
}

#-----------------------------------------------------------
# Create a user called device-deployer with a basic password
#-----------------------------------------------------------

resource "vault_generic_endpoint" "device-deployer" {
  path                 = "auth/${vault_auth_backend.userpass.path}/users/device-deployer"
  ignore_absent_fields = true

  data_json = <<EOT
{
  "token_policies": ["pki-reader-vault-policy"],
  "password": "Less-Secure-Cred!"
}
EOT
}

resource "vault_generic_endpoint" "jhow" {
  path                 = "auth/${vault_auth_backend.userpass.path}/users/jhow"
  ignore_absent_fields = true

  data_json = <<EOT
{
  "token_policies": ["user-creds-jhow-write-vault-policy"],
  "password": "jhow-Secure-Cred!"
}
EOT
}

resource "vault_generic_endpoint" "ubaumann" {
  path                 = "auth/${vault_auth_backend.userpass.path}/users/ubaumann"
  ignore_absent_fields = true

  data_json = <<EOT
{
  "token_policies": ["user-creds-ubaumann-write-vault-policy"],
  "password": "urs-Secure-Cred!"
}
EOT
}
