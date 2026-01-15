package list

import "github.com/charmbracelet/lipgloss/v2"

var boldStyle = lipgloss.NewStyle().Bold(true)

func (m *Model) SetWidth(width int) {
	m.width = width
}

func (m *Model) SetHeight(height int) {
	m.height = height
}

func buttonStyle(focused bool) lipgloss.Style {
	if focused {
		return lipgloss.NewStyle().
			Foreground(lipgloss.Color("#fff7db")).
			Background(lipgloss.Color("#888b7e")).
			Italic(true).
			Underline(true).
			MarginLeft(1).
			MarginRight(5).
			Padding(0, 1).
			Width(15)
	}

	return lipgloss.NewStyle().
		Foreground(lipgloss.Color("#fff7db")).
		Background(lipgloss.Color("#888b7e")).
		MarginLeft(1).
		MarginRight(5).
		Padding(0, 1).
		Width(15)
}

func headerBorderStyle(focused bool) lipgloss.Style {
	if focused {
		return lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			BorderForeground(lipgloss.Color("#9a9afa"))
	}
	return lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("#5f5fff"))
}

func (m *Model) View() string {
	// Header section
	titleView := boldStyle.Render("Vocab List")
	modeSwitchView := buttonStyle(m.HeaderSection.Focused()).Render("Load preset")
	headerSectionView := headerBorderStyle(m.HeaderSection.Focused()).
		Width(m.width).
		Render(lipgloss.JoinHorizontal(lipgloss.Center, titleView, modeSwitchView))

	return headerSectionView
}
