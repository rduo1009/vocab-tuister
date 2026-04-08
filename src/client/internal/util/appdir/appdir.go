// Get application directories such as config and cache.
//
// Adapted from https://github.com/emersion/go-appdir.
//
// The package provides platform-specific directory paths following OS conventions:
//   - macOS: Uses ~/Library directories
//   - Windows: Uses Local/Roaming AppData directories
//   - Linux/Unix: Follows XDG Base Directory specification
//
// If required environment variables (HOME, LOCALAPPDATA, etc.) are not set,
// the current directory (".") is used as a fallback.
//
// Example usage:
//
//	dirs := appdir.New("myapp")
//	configPath := dirs.UserConfig() // e.g., /home/user/.config/myapp on Linux
package appdir

import (
	_ "embed"
	"os"
	"path/filepath"
)

//go:embed default_sessionconfig.json
var defaultSessionconfig []byte

// Dirs requests application directories paths.
type Dirs interface {
	// Get the user-specific config directory.
	// Falls back to current directory if HOME or equivalent is not set.
	UserConfig() string
	// Get the user-specific cache directory.
	// Falls back to current directory if HOME or equivalent is not set.
	UserCache() string
	// Get the user-specific logs directory.
	// Falls back to current directory if HOME or equivalent is not set.
	UserLogs() string
	// Get the user-specific data directory.
	// Falls back to current directory if HOME or equivalent is not set.
	UserData() string
}

// New creates a new App with the provided name.
func New(author, name string) Dirs {
	return &dirs{author: author, name: name}
}

var AppDirs = New("rduo1009", "vocab-tuister")

func init() {
	err := os.MkdirAll(AppDirs.UserConfig(), 0o755)
	if err != nil {
		panic(err)
	}

	err = os.MkdirAll(filepath.Join(AppDirs.UserConfig(), "sessionconfig"), 0o755)
	if err != nil {
		panic(err)
	}

	err = os.WriteFile(
		filepath.Join(AppDirs.UserConfig(), "sessionconfig", "default_sessionconfig.json"),
		defaultSessionconfig,
		0o644,
	)
	if err != nil {
		panic(err)
	}

	err = os.MkdirAll(AppDirs.UserCache(), 0o755)
	if err != nil {
		panic(err)
	}

	err = os.MkdirAll(AppDirs.UserLogs(), 0o755)
	if err != nil {
		panic(err)
	}

	err = os.MkdirAll(AppDirs.UserData(), 0o755)
	if err != nil {
		panic(err)
	}
}
