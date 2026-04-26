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
	return m.configtui.FilepickerActive || m.listtui.FilepickerActive || m.listtui.SaveAsActive ||
		m.listtui.ModeDropdownActive
}

func (m *Model) OverlayView(width, height int) (view string, x, y int) {
	switch {
	case m.configtui.FilepickerActive:
		m.configtui.Filepicker.SetWidth(width / 2)
		m.configtui.Filepicker.SetHeight(height / 2)
		return m.configtui.Filepicker.View(width, height)

	case m.listtui.FilepickerActive:
		m.listtui.Filepicker.SetWidth(width / 2)
		m.listtui.Filepicker.SetHeight(height / 2)
		return m.listtui.Filepicker.View(width, height)

	case m.listtui.SaveAsActive:
		m.listtui.SaveAs.SetWidth(width / 2)
		m.listtui.SaveAs.SetHeight(height / 2)
		return m.listtui.SaveAs.View(width, height)

	case m.listtui.ModeDropdownActive:
		view = m.listtui.ModeDropdown.View()
		x = 12
		y = 4
		return view, x, y
	}

	panic("unreachable")
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

func (m *Model) getStatusStyle(s LoadStatus) lipgloss.Style {
	switch s {
	case StatusMissing:
		return m.styles.LoadSection.LabelMissing

	case StatusPending:
		return m.styles.LoadSection.LabelPending

	case StatusLoaded:
		return m.styles.LoadSection.LabelLoaded
	}
	panic("unreachable")
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
		style := m.getStatusStyle(status)

		labelView := m.styles.Text.Render(label + ":")
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

	loadSectionView := m.styles.NormalBorder(m.LoadSection.Focused()).
		Width(loadSectionWidth).
		Height(3).
		Align(lipgloss.Center).
		Render(lipgloss.JoinHorizontal(
			lipgloss.Center,
			renderStatus("List", m.LoadSection.ListStatus),
			m.styles.LoadSection.LabelSep.Render(" | "),
			renderStatus("Config", m.LoadSection.ConfigStatus),
			m.styles.LoadSection.LabelSep.Render(" | "),
			m.styles.Button(m.LoadSection.Enabled(), m.LoadSection.Focused()).Render("Load"),
		))

	m.configtui.SetWidth(m.width / 2)
	m.configtui.SetHeight(m.height - lipgloss.Height(loadSectionView) - 4)
	configView := m.configtui.View()

	rightView := lipgloss.JoinVertical(lipgloss.Left, configView, loadSectionView)

	return lipgloss.JoinHorizontal(lipgloss.Top, leftView, rightView)
}
