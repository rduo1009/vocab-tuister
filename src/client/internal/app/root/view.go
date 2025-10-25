package root

import (
	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/lipgloss"
)

func (m *Model) View() tea.View {
	currentPageModel := m.pages[m.pageOrder[m.currentPage]]

	tabsView := m.tabs.View()

	var helpView string
	if m.tabs.Focused() {
		helpView = m.help.View(m.keys)
	} else {
		helpView = m.help.View(currentPageModel.KeyMap())
	}

	currentPageModel.SetWidth(m.width)
	currentPageModel.SetHeight(m.height - lipgloss.Height(tabsView) - lipgloss.Height(helpView) - 4)
	pageView := currentPageModel.View()

	v := tea.NewView(lipgloss.JoinVertical(lipgloss.Left, tabsView, pageView, helpView))
	v.AltScreen = true
	v.WindowTitle = "Vocab Tester"
	return v
}
