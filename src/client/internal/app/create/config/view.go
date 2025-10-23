package config

import "github.com/charmbracelet/lipgloss/v2"

var (
	boldStyle   = lipgloss.NewStyle().Bold(true)
	buttonStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#fff7db")).
			Background(lipgloss.Color("#888b7e")).
			Padding(0, 3).
			MarginTop(1)
)

func (m *Model) SetWidth(width int) {
	m.width = width
	m.form.WithWidth(width - 4)
}

func (m *Model) SetHeight(height int) {
	m.height = height
	m.form.WithWidth(height - 2)
}

func (m *Model) View() string {
	headerBorderStyle := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("#5f5fff")). // purple border
		Width(m.width).
		// Height(m.height).
		Padding(1, 1)
	headerBorderFocusedStyle := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("#7d7dfb")). // purple border
		Width(m.width).
		// Height(m.height).
		Padding(1, 1)

	title := boldStyle.Render("Session Config")
	button := buttonStyle.Render("Load preset")
	var headerSection string
	if m.HeaderBorder.Focused() {
		headerSection = headerBorderFocusedStyle.Render(lipgloss.JoinHorizontal(lipgloss.Center, title, button))
	} else {
		headerSection = headerBorderStyle.Render(lipgloss.JoinHorizontal(lipgloss.Center, title, button))
	}

	formBorderStyle := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("#5f9fff")). // purple border
		Width(m.width).
		Height(m.height-lipgloss.Height(headerSection)).
		Padding(1, 2)
	formBorderFocusedStyle := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("#7caef9")). // purple border
		Width(m.width).
		Height(m.height-lipgloss.Height(headerSection)).
		Padding(1, 2)

	var formSection string
	if m.appStatus == CreateSessionConfig {
		if m.FormBorder.Focused() {
			formSection = formBorderFocusedStyle.Render("")
		} else {
			formSection = formBorderStyle.Render("")
		}
	} else {
		if m.FormBorder.Focused() {
			formSection = formBorderFocusedStyle.Render("")
		} else {
			formSection = formBorderStyle.Render("")
		}
	}

	return lipgloss.JoinVertical(lipgloss.Right, headerSection, formSection)
}
