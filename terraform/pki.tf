#----------------------------------
# Build a complete root/issuing PKI
#----------------------------------

## setup the mount point for the Root CA
#resource "vault_mount" "pki" {
#  path        = "pki"
#  type        = "pki"
#  description = "Problem of Network Root CA Mount"
#  default_lease_ttl_seconds = 86400
#  max_lease_ttl_seconds     = 315360000
#}
#
## create the actual root CA Cert and key
#resource "vault_pki_secret_backend_root_cert" "pon_root_g1" {
#  backend     = vault_mount.pki.path
#  type        = "internal"
#  common_name = "Problem Of Network Root G1"
#  ttl         = 315360000
#  issuer_name = "root-g1"
#  key_bits    = 4096
#}
#
## write this certificate to the terraform folder so we can use it elsewhere
#resource "local_file" "pon_root_g1_cert" {
#  content  = vault_pki_secret_backend_root_cert.pon_root_g1.certificate
#  filename = "root_ca_g1.crt"
#}
#
## optional: show this back to the user at runtime
#output "root_ca_certificate" {
#  value = vault_pki_secret_backend_root_cert.pon_root_g1.certificate
#}
#
## the backend issuer is the element of the vault pki that enables people to requests issuing certs against this root 
#resource "vault_pki_secret_backend_issuer" "pon_root_g1" {
#  backend                        = vault_mount.pki.path
#  issuer_ref                     = vault_pki_secret_backend_root_cert.pon_root_g1.issuer_id
#  issuer_name                    = vault_pki_secret_backend_root_cert.pon_root_g1.issuer_name
#  revocation_signature_algorithm = "SHA256WithRSA"
#}
#
## the backend role is the api parameters that are allowed to be used when signing issuing certs
#resource "vault_pki_secret_backend_role" "role" {
#  backend          = vault_mount.pki.path
#  name             = "root-sign-issuing-role"
#  allow_ip_sans    = true
#  key_type         = "rsa"
#  key_bits         = 4096
#  allow_subdomains = true
#  allow_any_name   = true
#}
#
## these config URLs are part of the vault pki ecosystem that clients can use to do ongoing checks that certs issued by this CA are not revoked before their expiry time 
#resource "vault_pki_secret_backend_config_urls" "config-urls" {
#  backend                 = vault_mount.pki.path
#  issuing_certificates    = ["http://vault.fatred.co.uk:8200/v1/pki/ca"]
#  crl_distribution_points = ["http://vault.fatred.co.uk:8200/v1/pki/crl"]
#}
#
## this is establishing the vault mountpoint for the issuing certificate authority
#resource "vault_mount" "pki_int" {
#  path        = "pki_int"
#  type        = "pki"
#  description = "Problem of Network Issuing CA Mount"
#
#  default_lease_ttl_seconds = 86400
#  max_lease_ttl_seconds     = 157680000
#}
#
## here we build a CSR (key never leaves vault) for that issuing CA
#resource "vault_pki_secret_backend_intermediate_cert_request" "csr-request" {
#  backend     = vault_mount.pki_int.path
#  type        = "internal"
#  common_name = "problemofnetwork-Issuing-G1"
#  key_bits    = 4096
#}
#
## optional: here we dump the certificate request contents out to the file system
## resource "local_file" "csr_request_cert" {
##   content  = vault_pki_secret_backend_intermediate_cert_request.csr-request.csr
##   filename = "pki_intermediate.csr"
## }
#
## here we are signing the issuing CA cert from the root CA backend using the CSR we just generated
#resource "vault_pki_secret_backend_root_sign_intermediate" "pon_issuing_g1" {
#  backend     = vault_mount.pki.path
#  common_name = "problemofnetwork-Issuing-G1"
#  csr         = vault_pki_secret_backend_intermediate_cert_request.csr-request.csr
#  format      = "pem_bundle"
#  ttl         = 15480000
#  issuer_ref  = vault_pki_secret_backend_root_cert.pon_root_g1.issuer_id
#}
#
## optional: write the issued certificate out to disk for use in chains
#resource "local_file" "pon_issuing_g1_cert" {
#  content  = vault_pki_secret_backend_root_sign_intermediate.pon_issuing_g1.certificate
#  filename = "pon_issuing_g1.cert.pem"
#}
#
## now that we have a signed cert from the root CA, we import that into the intermediate pki mountpoint ready for service
#resource "vault_pki_secret_backend_intermediate_set_signed" "pon_issuing_g1" {
#  backend     = vault_mount.pki_int.path
#  certificate = vault_pki_secret_backend_root_sign_intermediate.pon_issuing_g1.certificate
#}
#
## ...and ensure all the cert is applied to the backend issuer 
#resource "vault_pki_secret_backend_issuer" "pon_issuing_g1" {
#  backend     = vault_mount.pki_int.path
#  issuer_ref  = vault_pki_secret_backend_intermediate_set_signed.pon_issuing_g1.imported_issuers[0]
#  issuer_name = "problemofnetwork-Issuing-G1"
#}
#
## the intermediate backend role is where we will issue our end device certificates from
#resource "vault_pki_secret_backend_role" "pon_issuing_role" {
#  backend          = vault_mount.pki_int.path
#  issuer_ref       = vault_pki_secret_backend_issuer.pon_issuing_g1.issuer_ref
#  # this is the name we will use later to target this role
#  name             = "problemofnetwork-dot-com"
#  # valid for as little as 1d or up to 30d
#  ttl              = 86400
#  max_ttl          = 2592000
#  # we let the user request IP SANs (important in networking certs)
#  allow_ip_sans    = true
#  # we hook ourselves to rsa4096
#  key_type         = "rsa"
#  key_bits         = 4096
#  # limited to certs in the problemofnetwork.com domain
#  allowed_domains  = ["problemofnetwork.com"]
#  # we say we are ok with requests for _something_.problemofnetwork.com
#  allow_subdomains = true
#}
