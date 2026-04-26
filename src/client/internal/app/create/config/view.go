package config

import "charm.land/lipgloss/v2"

func (m *Model) SetWidth(width int) {
	m.width = width
}

func (m *Model) SetHeight(height int) {
	m.height = height
}

func (m *Model) View() string {
	// Header section
	titleView := m.styles.Bold.Render("Session Config")
	loadPresetButtonView := m.styles.Button(true, m.HeaderSection.Focused()).MarginLeft(1).Render("Load preset")
	headerSectionView := m.styles.NormalBorder(m.HeaderSection.Focused()).
		Width(m.width).
		Render(lipgloss.JoinHorizontal(lipgloss.Center, titleView, loadPresetButtonView))

	// Form section
	var formSectionView string
	if m.AppStatus == CreateSessionConfig {
		m.form.WithWidth(m.width - 2)
		m.form.WithHeight(m.height - lipgloss.Height(headerSectionView) - (len(m.form.Errors()) * 2))
		m.form.WithShowHelp(false)

		// consider wordwrapping, which would make the form height larger than it really should be
		m.form.WithHeight(min(lipgloss.Height(m.form.View()), m.height-lipgloss.Height(headerSectionView)))

		formSectionView = m.styles.NormalBorder(m.FormSection.Focused()).Padding(1, 2).
			Width(m.width).
			Height(m.height - lipgloss.Height(headerSectionView)).
			Render(m.form.View())
	} else {
		resetButtonView := m.styles.Button(true, m.ResetButton.Focused()).MarginLeft(1).Render("Reset form")

		m.jsonview.SetWidth(m.width - 6)
		m.jsonview.SetHeight(
			m.height - lipgloss.Height(headerSectionView) - lipgloss.Height(resetButtonView) - 2,
		)

		// NOTE: not specifying width here as jsonview will have the correct width from above
		formSectionView = m.styles.NormalBorder(m.FormSection.Focused()).Padding(1, 2).
			Height(m.height - lipgloss.Height(headerSectionView)).
			Render(lipgloss.JoinVertical(lipgloss.Left, resetButtonView, "", "", m.jsonview.View()))
	}

	return lipgloss.JoinVertical(lipgloss.Right, headerSectionView, formSectionView)
}
