// vault_operations/vault.go
package vault_operations

import (
	"context"
	"log"
	"os"

	vault "github.com/hashicorp/vault/api"
)

func InitVault() (*vault.Client, error) {
	// load a default vault config.
	config := vault.DefaultConfig()

	// Load Vault address from environment variable or use default if not set
	vaultAddr := os.Getenv("VAULT_ADDR")
	if vaultAddr == "" {
		log.Println("Vault address is missing. Using default of http://127.0.0.1:8200")
	} else {
		log.Printf("Using Vault address: %s", vaultAddr)
	}
	config.Address = vaultAddr

	client, err := vault.NewClient(config)
	if err != nil {
		log.Fatalf("unable to initialize Vault client: %v", err)
	}

	// Load Vault token from environment variable or use default if not set
	vaultToken := os.Getenv("VAULT_TOKEN")
	if vaultToken == "" {
		log.Fatalln("Vault token is required. Please set the VAULT_TOKEN environment variable.")
	}
	client.SetToken(vaultToken)

	return client, err
}

func WriteSecret(client *vault.Client, mount string, path string, secretData map[string]any) (bool, error) {
	ctx := context.Background()
	success := false

	// Write a secret
	_, err := client.KVv2(mount).Put(ctx, path, secretData)
	if err != nil {
		log.Fatalf("unable to write secret: %v", err)
	} else {
		success = true
		log.Println("Secret written successfully.")
	}
	return success, err
}

func ReadSecret(client *vault.Client, mount string, path string) (*map[string]any, error) {
	ctx := context.Background()
	secret, err := client.KVv2(mount).Get(ctx, path)
	return &secret.Data, err
}
