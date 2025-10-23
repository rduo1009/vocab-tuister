package root

import tea "github.com/charmbracelet/bubbletea/v2"

func (m *Model) Init() tea.Cmd {
	return m.pages[m.pageOrder[m.currentPage]].Init()
}
