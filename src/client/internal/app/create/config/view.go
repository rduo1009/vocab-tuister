package config

import "charm.land/lipgloss/v2"

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
			Padding(0, 1)
	}

	return lipgloss.NewStyle().
		Foreground(lipgloss.Color("#fff7db")).
		Background(lipgloss.Color("#888b7e")).
		MarginLeft(1).
		MarginRight(5).
		Padding(0, 1)
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

func formBorderStyle(focused bool) lipgloss.Style {
	if focused {
		return lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			BorderForeground(lipgloss.Color("#a4c6fb")).
			Padding(1, 2)
	}

	return lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("#5f9fff")).
		Padding(1, 2)
}

func (m *Model) View() string {
	// Header section
	titleView := m.styles.Bold.Render("Session Config")
	loadPresetButtonView := buttonStyle(m.HeaderSection.Focused()).Render("Load preset")
	headerSectionView := headerBorderStyle(m.HeaderSection.Focused()).
		Width(m.width).
		Render(lipgloss.JoinHorizontal(lipgloss.Center, titleView, loadPresetButtonView))

	// Form section
	var formSectionView string
	if m.AppStatus == CreateSessionConfig {
		m.form.WithWidth(m.width - 2)
		m.form.WithHeight(m.height - lipgloss.Height(headerSectionView) - (len(m.form.Errors()) * 2))
		m.form.WithShowHelp(false)

		// consider wordwrapping making the form height larger than it really should be
		m.form.WithHeight(min(lipgloss.Height(m.form.View()), m.height-lipgloss.Height(headerSectionView)))

		formSectionView = formBorderStyle(m.FormSection.Focused()).
			Width(m.width).
			Height(m.height - lipgloss.Height(headerSectionView)).
			Render(m.form.View())
	} else {
		resetButtonView := buttonStyle(m.ResetButton.Focused()).Render("Reset form")

		m.jsonview.SetWidth(m.width - 6)
		m.jsonview.SetHeight(
			m.height - lipgloss.Height(headerSectionView) - lipgloss.Height(resetButtonView) - 2,
		)

		// NOTE: not specifying width here as jsonview will have the correct width from above
		formSectionView = formBorderStyle(m.FormSection.Focused()).
			Height(m.height - lipgloss.Height(headerSectionView)).
			Render(lipgloss.JoinVertical(lipgloss.Left, resetButtonView, "", "", m.jsonview.View()))
	}

	return lipgloss.JoinVertical(lipgloss.Right, headerSectionView, formSectionView)
}
