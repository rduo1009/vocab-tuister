package listtui

import (
	"github.com/charmbracelet/bubbles/textarea"
	tea "github.com/charmbracelet/bubbletea"
)

func (m Model) Init() tea.Cmd {
	return tea.Batch(textarea.Blink, tea.SetWindowTitle("Create Vocab List"))
}
