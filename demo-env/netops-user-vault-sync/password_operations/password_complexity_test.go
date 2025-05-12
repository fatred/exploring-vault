// password_operations_test.go
package password_operations

import (
	"testing"
)

func TestCheckPasswordComplexity(t *testing.T) {
	tests := []struct {
		name     string
		password string
		expected bool
	}{
		{
			name:     "Valid password with all conditions",
			password: "Password123456!",
			expected: true,
		},
		{
			name:     "Valid password with lowercase digit and special character",
			password: "password123456!",
			expected: true,
		},
		{
			name:     "Valid password with lowercase upper and special character",
			password: "Passworddddddd!",
			expected: true,
		},
		{
			name:     "Invalid password missing lowercase letter",
			password: "PASSWORD1234567!",
			expected: false,
		},
		{
			name:     "Invalid password missing special character",
			password: "Password1234567",
			expected: false,
		},
		{
			name:     "Invalid password missing uppercase letter and digit",
			password: "passworddddddd!",
			expected: false,
		},
		{
			name:     "Invalid password too short",
			password: "Pass1!",
			expected: false,
		},
		{
			name:     "Invalid password missing all required characters",
			password: "pass",
			expected: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CheckPasswordComplexity(tt.password)
			if result != tt.expected {
				t.Errorf("expected %v, got %v", tt.expected, result)
			}
		})
	}
}
