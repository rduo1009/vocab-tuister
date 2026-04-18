package list

import (
	"charm.land/lipgloss/v2"
)

func (m *Model) SetWidth(width int) {
	m.width = width
}

func (m *Model) SetHeight(height int) {
	m.height = height
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

func (m *Model) View() string {
	// Header section
	titleView := m.styles.Bold.Render("Vocab List")
	modeSwitchView := m.styles.Button(true, m.HeaderSection.Focused()).
		MarginLeft(1).
		Width(14).
		Render(m.AppStatus.String())
	headerSectionView := m.styles.NormalBorder(m.HeaderSection.Focused()).
		Width(m.width).
		Render(lipgloss.JoinHorizontal(lipgloss.Center, titleView, modeSwitchView))

	// Footer section
	footerView := m.styles.Bold.Render("List:")
	selectListView := m.styles.Button(true, m.SelectButton.Focused()).
		MarginLeft(1).
		Render(selectListText(m.AppStatus))
	footerSectionView := m.styles.NormalBorder(m.SelectButton.Focused()).
		Width(m.width).
		Render(lipgloss.JoinHorizontal(lipgloss.Center, footerView, selectListView))

	// Editor section
	m.VocabEditor.SetSize(
		m.width-6,
		m.height-lipgloss.Height(headerSectionView)-lipgloss.Height(footerSectionView)+2,
	)
	editorSectionView := m.styles.NormalBorder(m.VocabEditor.Focused()).Padding(0, 2).
		Width(m.width).
		Height(m.height - lipgloss.Height(headerSectionView) - lipgloss.Height(footerSectionView) + 2).
		Render(m.VocabEditor.View())

	return lipgloss.JoinVertical(lipgloss.Right, headerSectionView, editorSectionView, footerSectionView)
}
