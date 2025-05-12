package main

import (
	"encoding/base64"
	"flag"
	"fmt"
	"log"
	"os"

	"github.com/fatred/exploring-vault/demo-env/netops-user-vault-sync/password_operations"
	"github.com/fatred/exploring-vault/demo-env/netops-user-vault-sync/vault_operations"
)

func main() {
	// Define the command-line argument for the password
	password := flag.String("password", "", "Password to hash")
	flag.Parse()

	// use input or prompt for the password to encode
	var inputPassword string
	if *password != "" {
		// we have a password on the cli args
		inputPassword = *password
	} else {
		// we have to ask for a password
		inputPassword = password_operations.PromptPassword()
	}

	// Generate salt and encode it to base64
	salt, err := password_operations.GenerateSalt()
	if err != nil {
		log.Fatalf("error generating salt: %v", err)
	}
	encodedSalt := []byte(base64.StdEncoding.EncodeToString(salt))

	// Argon2 first
	// Hash password with b64 encoded salt
	argon2HashedPassword := password_operations.GenerateArgon2Hash(inputPassword, encodedSalt)
	// encode the hash to base64
	nokiaEncodedPassword := base64.StdEncoding.EncodeToString(argon2HashedPassword)

	// store it to use it later
	nokiaSRLHash := fmt.Sprintf("$ar2$%s$%s", encodedSalt, nokiaEncodedPassword)
	// tell the world what we found.
	fmt.Printf("SR Linux formatted hash+salt: %s\n", nokiaSRLHash)

	client, err := vault_operations.InitVault()
	if err != nil {
		log.Fatalf("unable to initialize Vault client: %v", err)
	} else {
		log.Println("Vault client initialized successfully.")
	}

	secretData := map[string]any{
		"nokia_ar2": nokiaSRLHash,
	}
	_, _ = vault_operations.WriteSecret(client, "user-creds", os.Getenv("USER"), secretData)

	testSecret, err := vault_operations.ReadSecret(client, "user-creds", os.Getenv("USER"))
	if err != nil {
		log.Fatalf("unable to read secret: %v", err)
	} else {
		log.Printf("Read secret: %+v", testSecret)
	}
}
