package listtui

import (
	"github.com/charmbracelet/bubbles/help"
	"github.com/charmbracelet/bubbles/textarea"
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
	ti.CharLimit = -1
	ti.Placeholder = "Write your vocab here..."
	ti.Focus()

	return Model{
		textarea: ti,
		help:     help.New(),
		keys:     DefaultKeyMap,
		filePath: filePath,
		err:      nil,
	}
}
