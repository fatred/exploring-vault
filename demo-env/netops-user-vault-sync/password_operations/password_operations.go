// password_operations.go
package password_operations

import (
	"crypto/rand"
	"fmt"
	"log"
	"os"
	"regexp"

	"golang.org/x/crypto/argon2"
	"golang.org/x/term"
)

const (
	saltLen = 16
	keyLen  = 16
	time    = 1
	memory  = 64 * 1024
	threads = 1
)

func GenerateSalt() ([]byte, error) {
	// generate some random salt to use for the hash creation
	salt := make([]byte, saltLen)
	n, err := rand.Read(salt)
	if n != saltLen || err != nil {
		return nil, fmt.Errorf("error generating random salt: %v", err)
	}
	return salt, nil
}

func GenerateArgon2Hash(password string, salt []byte) []byte {
	// generate an Argon2 hash using the password string, the salt bytes and the constants above
	return argon2.Key([]byte(password), salt, time, memory, threads, keyLen)
}

// CheckPasswordComplexity checks if the password meets the defined complexity rules.
func CheckPasswordComplexity(password string) bool {
	// Define the complexity rules
	minLength := 14
	hasLower := regexp.MustCompile(`[a-z]`).MatchString
	hasSpecial := regexp.MustCompile(`[!@#$%^&*(),.?":{}|<>]`).MatchString
	hasUpper := regexp.MustCompile(`[A-Z]`).MatchString
	hasDigit := regexp.MustCompile(`[0-9]`).MatchString

	// Check the rules
	if len(password) < minLength {
		return false
	}
	if !hasLower(password) {
		return false
	}
	if !hasSpecial(password) {
		return false
	}
	if !hasUpper(password) && !hasDigit(password) {
		return false
	}
	return true
}

func PromptPassword() string {
	// Read password interactively
	var password1, password2 string
	for {
		fmt.Print("Enter password: ")
		bytePassword1, err := term.ReadPassword(int(os.Stdin.Fd()))
		if err != nil {
			log.Fatalf("error reading password: %v", err)
		}
		password1 = string(bytePassword1)

		if !CheckPasswordComplexity(password1) {
			fmt.Println("Password should meet complexity requirements (>=15 chars, lower and special, plus one or both of upper and digit). Please try again.")
			fmt.Print("Enter password: ")
			bytePassword1, err := term.ReadPassword(int(os.Stdin.Fd()))
			if err != nil {
				log.Fatalf("error reading password: %v", err)
			}
			password1 = string(bytePassword1)
			fmt.Println() // Print a new line after the password input
		}

		fmt.Print("Confirm password: ")
		bytePassword2, err := term.ReadPassword(int(os.Stdin.Fd()))
		if err != nil {
			log.Fatalf("error reading password: %v", err)
		}
		password2 = string(bytePassword2)
		fmt.Println() // Print a new line after the password input

		if password1 == password2 {
			return password1
		} else {
			fmt.Println("Passwords do not match. Please try again.")
		}
	}
}
