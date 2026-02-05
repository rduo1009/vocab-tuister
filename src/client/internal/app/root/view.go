package root

import (
	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"
)

var dimPageStyle = lipgloss.NewStyle().Foreground(lipgloss.Color("8"))

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
	fullView := lipgloss.JoinVertical(lipgloss.Left, tabsView, pageView, helpView)

	var compositor *lipgloss.Compositor
	if currentPageModel.HasOverlay() {
		dimPageView := dimPageStyle.Render(fullView)
		compositor = lipgloss.NewCompositor(lipgloss.NewLayer(dimPageView))

		overlayPageView := currentPageModel.OverlayView(m.width/2, m.height/2)
		overlayHelpView := m.overlayHelp.View(currentPageModel.OverlayKeyMap())
		overlayView := lipgloss.Place(m.width, m.height,
			lipgloss.Center, lipgloss.Center,
			lipgloss.JoinVertical(lipgloss.Left, overlayPageView, overlayHelpView),
			lipgloss.WithWhitespaceChars(" "),
		)

		compositor.AddLayers(lipgloss.NewLayer(overlayView))
	} else {
		compositor = lipgloss.NewCompositor(lipgloss.NewLayer(fullView))
	}

	v := tea.NewView(compositor.Render())
	v.AltScreen = true
	v.WindowTitle = "Vocab Tester"
	return v
}
