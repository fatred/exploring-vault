#---------------------------------
# Issue a cert "the terraform way"
#---------------------------------

## here we make a request for a "real" cert
#resource "vault_pki_secret_backend_cert" "test-problemofnetwork-dot-com" {
#  # target the issuer
#  issuer_ref  = vault_pki_secret_backend_issuer.pon_issuing_g1.issuer_ref
#  # using the issuing backend
#  backend     = vault_pki_secret_backend_role.pon_issuing_role.backend
#  # and the issuing role
#  name        = vault_pki_secret_backend_role.pon_issuing_role.name
#  # for a common name in our scope
#  common_name = "test.problemofnetwork.com"
#  # with a 1d ttl
#  ttl         = 3600
#  # to be used later to revoke it as no longer valid 
#  #revoke     = true
#}
#
#output "test-problemofnetwork-dot-com_cert" {
#  value = vault_pki_secret_backend_cert.test-problemofnetwork-dot-com.certificate
#}
#
#output "test-problemofnetwork-dot-com_issuing_ca" {
#  value = vault_pki_secret_backend_cert.test-problemofnetwork-dot-com.issuing_ca
#}
#
#output "test-problemofnetwork-dot-com_serial_number" {
#  value = vault_pki_secret_backend_cert.test-problemofnetwork-dot-com.serial_number
#}
#
