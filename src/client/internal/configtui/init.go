package configtui

import (
	"github.com/charmbracelet/bubbles/v2/textinput"
	tea "github.com/charmbracelet/bubbletea/v2"
)

func (m model) Init() (tea.Model, tea.Cmd) {
	return m, textinput.Blink
}
