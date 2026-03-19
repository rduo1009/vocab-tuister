//go:build darwin

package appdir

import (
	"os"
	"path/filepath"
	"testing"
)

func TestDarwinDirs(t *testing.T) {
	origHome := os.Getenv("HOME")
	defer os.Setenv("HOME", origHome)

	home := "/Users/testuser"
	os.Setenv("HOME", home)

	d := &dirs{name: "myapp"}

	tests := []struct {
		name     string
		got      string
		expected string
	}{
		{"UserConfig", d.UserConfig(), filepath.Join(home, "Library", "Application Support", "myapp")},
		{"UserCache", d.UserCache(), filepath.Join(home, "Library", "Caches", "myapp")},
		{"UserLogs", d.UserLogs(), filepath.Join(home, "Library", "Logs", "myapp")},
		{"UserData", d.UserData(), filepath.Join(home, "Library", "Application Support", "myapp")},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if tt.got != tt.expected {
				t.Errorf("expected %q, got %q", tt.expected, tt.got)
			}
		})
	}
}

func TestDarwinDirsNoHome(t *testing.T) {
	origHome := os.Getenv("HOME")
	defer os.Setenv("HOME", origHome)

	os.Unsetenv("HOME")

	d := &dirs{name: "myapp"}
	home := "."

	tests := []struct {
		name     string
		got      string
		expected string
	}{
		{"UserConfig", d.UserConfig(), filepath.Join(home, "Library", "Application Support", "myapp")},
		{"UserCache", d.UserCache(), filepath.Join(home, "Library", "Caches", "myapp")},
		{"UserLogs", d.UserLogs(), filepath.Join(home, "Library", "Logs", "myapp")},
		{"UserData", d.UserData(), filepath.Join(home, "Library", "Application Support", "myapp")},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if tt.got != tt.expected {
				t.Errorf("expected %q, got %q", tt.expected, tt.got)
			}
		})
	}
}
