package listtui

import (
	"github.com/charmbracelet/bubbles/v2/help"
	"github.com/charmbracelet/bubbles/v2/textarea"
)

type model struct {
	textarea textarea.Model
	keys     KeyMap
	help     help.Model
	filePath string
	width    int
	height   int
	err      error
}

func InitialModel(filePath string) model { //nolint:revive
	ti := textarea.New()
	ti.Placeholder = "Write vocab list here..."
	ti.Focus()

	return model{
		keys:     DefaultKeyMap,
		help:     help.New(),
		textarea: ti,
		filePath: filePath,
	}
}
