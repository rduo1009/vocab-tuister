package appdir

import (
	"os"
	"path/filepath"
)

type dirs struct {
	author string
	name   string
}

func (d *dirs) UserConfig() string {
	home := os.Getenv("HOME")
	if home == "" {
		home = "."
	}

	return filepath.Join(home, "Library", "Application Support", d.name)
}

func (d *dirs) UserCache() string {
	home := os.Getenv("HOME")
	if home == "" {
		home = "."
	}

	return filepath.Join(home, "Library", "Caches", d.name)
}

func (d *dirs) UserLogs() string {
	home := os.Getenv("HOME")
	if home == "" {
		home = "."
	}

	return filepath.Join(home, "Library", "Logs", d.name)
}

func (d *dirs) UserData() string {
	home := os.Getenv("HOME")
	if home == "" {
		home = "."
	}

	return filepath.Join(home, "Library", "Application Support", d.name)
}
