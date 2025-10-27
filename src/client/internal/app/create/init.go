package create

import tea "github.com/charmbracelet/bubbletea/v2"

func (m *Model) Init() tea.Cmd {
	return tea.Batch(m.configtui.Init(), m.configtuiFilepicker.Init())
}
