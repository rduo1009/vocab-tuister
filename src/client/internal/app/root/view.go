package root

import (
	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"
)

var dimPageStyle = lipgloss.NewStyle().Faint(true)

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

	var layers []*lipgloss.Layer
	if currentPageModel.HasOverlay() {
		dimPageLayer := lipgloss.NewLayer(dimPageStyle.Render(fullView))

		overlayPageView, x, y := currentPageModel.OverlayView(m.width, m.height)
		overlayLayer := lipgloss.NewLayer(overlayPageView).X(x).Y(y)

		layers = []*lipgloss.Layer{dimPageLayer, overlayLayer}
	} else {
		layers = []*lipgloss.Layer{lipgloss.NewLayer(fullView)}
	}

	if m.errorDialog.Visible() {
		m.errorDialog.SetWidth(m.width)
		m.errorDialog.SetHeight(m.height)

		dialogView := m.errorDialog.View()
		dialogLayer := lipgloss.NewLayer(dialogView).X(m.width - m.width/4).Y(0)

		layers = append(layers, dialogLayer)
	}

	v := tea.NewView(lipgloss.NewCompositor(layers...).Render())
	v.AltScreen = true
	v.WindowTitle = "Vocab Tester"

	return v
}
