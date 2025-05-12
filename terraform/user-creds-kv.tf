#--------------------------------
# Create a new secret mount point
# for key/value store
#--------------------------------

resource "vault_mount" "user-creds" {
  path        = "user-creds"
  type        = "kv"
  options     = { version = "2" }
}