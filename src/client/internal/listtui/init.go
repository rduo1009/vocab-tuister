package listtui

import (
	"github.com/charmbracelet/bubbles/v2/textarea"
	tea "github.com/charmbracelet/bubbletea/v2"
)

func (m Model) Init() (tea.Model, tea.Cmd) {
	return m, tea.Batch(textarea.Blink, tea.SetWindowTitle("Create Vocab List"))
}
