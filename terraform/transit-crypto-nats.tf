# # transit-crypto-nats.tf
# resource "vault_mount" "transit_nats" {
#   path        = "transit-nats"
#   type        = "transit"
#   description = "This is a transit secret engine mount for NATS message encryption"

#   options = {
#     convergent_encryption = false
#   }
# }

# resource "vault_transit_secret_backend_key" "transit_nats_demo_key" {
#   backend = vault_mount.transit_nats.path
#   name    = "demo_key"
# }

# #-----------------------------------------------------
# # Create a policy that can encrypt and decrypt content
# #-----------------------------------------------------

# resource "vault_policy" "transit_nats_client_policy" {
#   name = "transit-nats-client-policy"

#   policy = <<EOT
# path "transit-nats/encrypt/demo_key" {
#    capabilities = [ "update" ]
# }

# path "transit-nats/decrypt/demo_key" {
#    capabilities = [ "update" ]
# }
# EOT
# }

# #--------------------------------------------------------
# # Create a user called nats-worker1 with a basic password
# #--------------------------------------------------------

# resource "vault_generic_endpoint" "nats-worker1" {
#   path                 = "auth/${vault_auth_backend.userpass.path}/users/nats-worker1"
#   ignore_absent_fields = true

#   data_json = <<EOT
# {
#   "token_policies": ["transit-nats-client-policy"],
#   "password": "Less-Secure-Cred!"
# }
# EOT
# }

# #--------------------------------------------------------
# # Create a user called nats-worker2 with a basic password
# #--------------------------------------------------------

# resource "vault_generic_endpoint" "nats-worker2" {
#   path                 = "auth/${vault_auth_backend.userpass.path}/users/nats-worker2"
#   ignore_absent_fields = true

#   data_json = <<EOT
# {
#   "token_policies": ["transit-nats-client-policy"],
#   "password": "Less-Secure-Cred!"
# }
# EOT
# }
