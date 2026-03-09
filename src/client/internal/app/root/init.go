package root

import tea "charm.land/bubbletea/v2"

func (m *Model) Init() tea.Cmd {
	return m.pages[m.pageOrder[m.currentPage]].Init()
}
