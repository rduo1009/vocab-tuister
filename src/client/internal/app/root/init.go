package root

import tea "charm.land/bubbletea/v2"

func (m *Model) Init() tea.Cmd {
	currentPageModel := m.pages[m.pageOrder[m.currentPage]]
	return currentPageModel.Init()
}
