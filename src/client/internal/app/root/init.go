package root

import tea "github.com/charmbracelet/bubbletea/v2"

func (m *Model) Init() tea.Cmd {
	currentPageModel := m.pages[m.pageOrder[m.currentPage]]
	return currentPageModel.Init()
}
