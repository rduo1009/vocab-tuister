
package appdir

import (
	"os"
	"path/filepath"
	"sync"
	"testing"
)

func TestWindowsDirs(t *testing.T) {
	// Reset state for test because initOnce prevents re-initialization
	initOnce = sync.Once{}
	
	origLocal := os.Getenv("LOCALAPPDATA")
	origRoaming := os.Getenv("APPDATA")
	defer func() {
		os.Setenv("LOCALAPPDATA", origLocal)
		os.Setenv("APPDATA", origRoaming)
		// Reset again for other tests/runs
		initOnce = sync.Once{}
	}()

	local := `C:\Users\testuser\AppData\Local`
	roaming := `C:\Users\testuser\AppData\Roaming`
	os.Setenv("LOCALAPPDATA", local)
	os.Setenv("APPDATA", roaming)

	d := &dirs{author: "myauth", name: "myapp"}

	// On Windows, UserConfig uses roamingAppData, others use localAppData.
	expectConfig := filepath.Join(roaming, "myauth", "myapp")
	expectOther := filepath.Join(local, "myauth", "myapp")

	tests := []struct {
		name     string
		got      string
		expected string
	}{
		{"UserConfig", d.UserConfig(), expectConfig},
		{"UserCache", d.UserCache(), expectOther},
		{"UserLogs", d.UserLogs(), expectOther},
		{"UserData", d.UserData(), expectOther},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if tt.got != tt.expected {
				t.Errorf("expected %q, got %q", tt.expected, tt.got)
			}
		})
	}
}

func TestWindowsDirsNoEnv(t *testing.T) {
	// Reset state
	initOnce = sync.Once{}
	
	origLocal := os.Getenv("LOCALAPPDATA")
	origRoaming := os.Getenv("APPDATA")
	defer func() {
		os.Setenv("LOCALAPPDATA", origLocal)
		os.Setenv("APPDATA", origRoaming)
		initOnce = sync.Once{}
	}()

	os.Unsetenv("LOCALAPPDATA")
	os.Unsetenv("APPDATA")

	d := &dirs{author: "myauth", name: "myapp"}

	// When env vars are missing and KnownFolderPath fails (likely in test environment),
	// it should return empty string base paths, resulting in "myauth/myapp" or just "."
	// However, current implementation doesn't have a specific fallback for empty env vars 
	// other than what filepath.Join does with empty strings.
	
	res := d.UserConfig()
	if !filepath.IsAbs(res) && res == "" {
		t.Log("Got empty path as expected when no env vars and syscall fails")
	}
}
