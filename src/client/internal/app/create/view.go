package create

import (
	"charm.land/lipgloss/v2"
)

func (m *Model) SetWidth(width int) {
	m.width = width
}

func (m *Model) SetHeight(height int) {
	m.height = height
}

func (m *Model) HasOverlay() bool {
	return m.configtuiFilepickerActive || m.listtuiFilepickerActive || m.listtuiSaveAsActive ||
		m.listtuiModeDropdownActive
}

func (m *Model) OverlayView(width, height int) (view string, x, y int) {
	switch {
	case m.configtuiFilepickerActive:
		m.configtuiFilepicker.SetWidth(width / 2)
		m.configtuiFilepicker.SetHeight(height / 2)
		return m.configtuiFilepicker.View(width, height)

	case m.listtuiFilepickerActive:
		m.listtuiFilepicker.SetWidth(width / 2)
		m.listtuiFilepicker.SetHeight(height / 2)
		return m.listtuiFilepicker.View(width, height)

	case m.listtuiSaveAsActive:
		m.listtuiSaveAs.SetWidth(width / 2)
		m.listtuiSaveAs.SetHeight(height / 2)
		return m.listtuiSaveAs.View(width, height)

	case m.listtuiModeDropdownActive:
		view = m.listtuiModeDropdown.View()
		x = 12
		y = 4
		return view, x, y
	}

	panic("unreachable")
}

func loadBorderStyle(focused bool) lipgloss.Style {
	if focused {
		return lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			BorderForeground(lipgloss.Color("#fdffcd"))
	}

	return lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("#f3ff00"))
}

func statusSymbol(s LoadStatus) string {
	switch s {
	case StatusMissing:
		return "×"

	case StatusPending:
		return "~"

	case StatusLoaded:
		return "✓"

	default:
		panic("unreachable")
	}
}

func statusText(s LoadStatus) string {
	switch s {
	case StatusMissing:
		return "missing"

	case StatusPending:
		return "pending"

	case StatusLoaded:
		return "loaded"

	default:
		panic("unreachable")
	}
}

var (
	missingStyle = lipgloss.NewStyle().Foreground(lipgloss.Color("#ff5555"))
	pendingStyle = lipgloss.NewStyle().Foreground(lipgloss.Color("#f1fa8c"))
	loadedStyle  = lipgloss.NewStyle().Foreground(lipgloss.Color("#50fa7b"))
	sepStyle     = lipgloss.NewStyle().Foreground(lipgloss.Color("#666666"))
)

func getStatusStyle(s LoadStatus) lipgloss.Style {
	switch s {
	case StatusMissing:
		return missingStyle

	case StatusPending:
		return pendingStyle

	case StatusLoaded:
		return loadedStyle

	default:
		return lipgloss.NewStyle()
	}
}

func buttonStyle(focused, enabled bool) lipgloss.Style {
	style := lipgloss.NewStyle().
		Foreground(lipgloss.Color("#fff7db")).
		Background(lipgloss.Color("#888b7e")).
		Padding(0, 1)

	if !enabled {
		return style.Foreground(lipgloss.Color("#a9a9a9")).Background(lipgloss.Color("#555555"))
	}

	if focused {
		return style.Italic(true).Underline(true)
	}

	return style
}

func (m *Model) View() string {
	m.listtui.SetWidth(m.width / 2)
	m.listtui.SetHeight(m.height - 4)
	leftView := m.listtui.View()

	loadSectionWidth := m.width / 2
	statusSpace := (loadSectionWidth - 16) / 2
	renderStatus := func(label string, status LoadStatus) string {
		symbol := statusSymbol(status)
		text := statusText(status)
		style := getStatusStyle(status)

		labelView := label + ":"
		textView := style.Render(text)
		symbolView := style.Render(symbol)

		// Option 1: Label + Full Word
		full := labelView + " " + textView
		// Option 2: Label + Symbol
		mid := labelView + " " + symbolView

		if statusSpace >= lipgloss.Width(full) {
			return full
		} else if statusSpace >= lipgloss.Width(mid) {
			return mid
		}
		// Fallback: just symbol
		return symbolView
	}

	loadSectionView := loadBorderStyle(m.LoadSection.Focused()).
		Width(loadSectionWidth).
		Height(3).
		Align(lipgloss.Center).
		Render(lipgloss.JoinHorizontal(
			lipgloss.Center,
			renderStatus("List", m.LoadSection.ListStatus),
			sepStyle.Render(" | "),
			renderStatus("Config", m.LoadSection.ConfigStatus),
			sepStyle.Render(" | "),
			buttonStyle(m.LoadSection.Focused(), m.LoadSection.Enabled()).Render("Load"),
		))

	m.configtui.SetWidth(m.width / 2)
	m.configtui.SetHeight(m.height - lipgloss.Height(loadSectionView) - 4)
	configView := m.configtui.View()

	rightView := lipgloss.JoinVertical(lipgloss.Left, configView, loadSectionView)

	return lipgloss.JoinHorizontal(lipgloss.Top, leftView, rightView)
}
