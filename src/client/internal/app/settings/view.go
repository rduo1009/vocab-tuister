package settings

import "charm.land/lipgloss/v2"

func (m *Model) SetWidth(width int) {
	m.width = width
}

func (m *Model) SetHeight(height int) {
	m.height = height
}

func (m *Model) HasOverlay() bool {
	return false
}

func (m *Model) OverlayView(width, height int) (view string, x, y int) {
	panic("wip")
}

func (m *Model) View() string {
	style := m.styles.NormalBorder(m.Focused())

	content := lipgloss.Place(
		m.width-2,
		m.height-2,
		lipgloss.Center,
		lipgloss.Center,
		lipgloss.NewStyle().
			Padding(1, 3).
			Render("Work In Progress"),
		lipgloss.WithWhitespaceChars("/"),
		lipgloss.WithWhitespaceStyle(lipgloss.NewStyle().Foreground(lipgloss.Color("#383838"))),
	)

	return style.
		Width(m.width).
		Height(m.height).
		Render(content)
}
