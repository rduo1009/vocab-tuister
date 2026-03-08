package list

import (
	"charm.land/lipgloss/v2"
)

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
			Padding(0, 1)
	}

	return lipgloss.NewStyle().
		Foreground(lipgloss.Color("#fff7db")).
		Background(lipgloss.Color("#888b7e")).
		MarginLeft(1).
		Padding(0, 1)
}

func headerBorderStyle(focused bool) lipgloss.Style {
	if focused {
		return lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			BorderForeground(lipgloss.Color("#a9eaa9"))
	}

	return lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("#2cb42c"))
}

func editorBorderStyle(focused bool) lipgloss.Style {
	if focused {
		return lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			BorderForeground(lipgloss.Color("#c6fba4")).
			Padding(0, 2)
	}

	return lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("#80ff2c")).
		Padding(0, 2)
}

func selectListText(status createListStatus) string {
	switch status {
	case InbuiltList:
		return "Select inbuilt list..."

	case LocalList:
		return "Select local list..."

	case CustomList:
		return "Save list..."
	}

	panic("unreachable")
}

func footerBorderStyle(focused bool) lipgloss.Style {
	if focused {
		return lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			BorderForeground(lipgloss.Color("#ffd19a"))
	}

	return lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("#ff8c00"))
}

func (m *Model) View() string {
	// Header section
	titleView := boldStyle.Render("Vocab List")
	modeSwitchView := buttonStyle(m.HeaderSection.Focused()).Width(14).Render(m.appStatus.String())
	headerSectionView := headerBorderStyle(m.HeaderSection.Focused()).
		Width(m.width).
		Render(lipgloss.JoinHorizontal(lipgloss.Center, titleView, modeSwitchView))

	// Footer section
	footerView := boldStyle.Render("List:")
	selectListView := buttonStyle(m.SelectButton.Focused()).Render(selectListText(m.appStatus))
	footerSectionView := footerBorderStyle(m.SelectButton.Focused()).
		Width(m.width).
		Render(lipgloss.JoinHorizontal(lipgloss.Center, footerView, selectListView))

	// Editor section
	m.VocabEditor.SetSize(
		m.width-6,
		m.height-lipgloss.Height(headerSectionView)-lipgloss.Height(footerSectionView)+2,
	)
	editorSectionView := editorBorderStyle(m.VocabEditor.Focused()).
		Width(m.width).
		Height(m.height - lipgloss.Height(headerSectionView) - lipgloss.Height(footerSectionView) + 2).
		Render(m.VocabEditor.View())

	return lipgloss.JoinVertical(lipgloss.Right, headerSectionView, editorSectionView, footerSectionView)
}
