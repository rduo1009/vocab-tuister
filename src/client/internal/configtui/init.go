package configtui

import (
	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
)

func (m Model) Init() tea.Cmd {
	return tea.Batch(textinput.Blink, tea.SetWindowTitle("Create Session Config"))
}
