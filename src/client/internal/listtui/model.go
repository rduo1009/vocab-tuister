package listtui

import (
	"github.com/charmbracelet/bubbles/v2/help"
	"github.com/charmbracelet/bubbles/v2/textarea"
)

type Model struct {
	textarea textarea.Model
	help     help.Model
	keys     KeyMap
	filePath string
	width    int
	height   int
	err      error
}

func InitialModel(filePath string) Model {
	ti := textarea.New()
	ti.Placeholder = "Write vocab list here..."
	ti.Focus()

	return Model{
		textarea: ti,
		help:     help.New(),
		keys:     DefaultKeyMap,
		filePath: filePath,
		err:      nil,
	}
}
