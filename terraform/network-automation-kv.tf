#--------------------------------
# Create a new secret mount point
# for key/value store
#--------------------------------

resource "vault_mount" "network-automation" {
  path        = "network-automation"
  type        = "kv"
  options     = { version = "2" }
}