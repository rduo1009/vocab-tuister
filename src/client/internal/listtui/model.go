package listtui

import "github.com/charmbracelet/bubbles/v2/textarea"

type model struct {
	textarea textarea.Model
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
		textarea: ti,
		filePath: filePath,
	}
}
