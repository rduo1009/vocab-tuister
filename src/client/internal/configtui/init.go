package configtui

import (
	"github.com/charmbracelet/bubbles/v2/textinput"
	tea "github.com/charmbracelet/bubbletea/v2"
)

func (m Model) Init() (tea.Model, tea.Cmd) {
	return m, tea.Batch(textinput.Blink, tea.SetWindowTitle("Create Session Config"))
}
