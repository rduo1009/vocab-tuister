package create

import (
	"charm.land/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
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

func statusSymbol(s VerifyStatus, styles *styles.StylesWrapper) string {
	switch s {
	case StatusMissing:
		return styles.Icons.Cross

	case StatusPending:
		return "~"

	case StatusVerified:
		return styles.Icons.Checkmark

	default:
		panic("unreachable")
	}
}

func statusText(s VerifyStatus) string {
	switch s {
	case StatusMissing:
		return "missing"

	case StatusPending:
		return "pending"

	case StatusVerified:
		return "verified"

	default:
		panic("unreachable")
	}
}

func (m *Model) getStatusStyle(s VerifyStatus) lipgloss.Style {
	switch s {
	case StatusMissing:
		return m.styles.VerifySection.LabelMissing

	case StatusPending:
		return m.styles.VerifySection.LabelPending

	case StatusVerified:
		return m.styles.VerifySection.LabelVerified
	}

	panic("unreachable")
}

func (m *Model) View() string {
	m.listtui.SetWidth(m.width / 2)
	m.listtui.SetHeight(m.height - 4)
	leftView := m.listtui.View()

	verifySectionWidth := m.width / 2
	statusSpace := (verifySectionWidth - 16) / 2
	renderStatus := func(label string, status VerifyStatus) string {
		symbol := statusSymbol(status, m.styles)
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

	verifySectionView := m.styles.NormalBorder(m.VerifySection.Focused()).
		Width(verifySectionWidth).
		Height(3).
		Align(lipgloss.Center).
		Render(lipgloss.JoinHorizontal(
			lipgloss.Center,
			renderStatus("List", m.VerifySection.ListStatus),
			m.styles.VerifySection.LabelSep.Render(" | "),
			renderStatus("Config", m.VerifySection.ConfigStatus),
			m.styles.VerifySection.LabelSep.Render(" | "),
			m.styles.Button(m.VerifySection.Enabled(), m.VerifySection.Focused()).Render("Verify"),
		))

	m.configtui.SetWidth(m.width / 2)
	m.configtui.SetHeight(m.height - lipgloss.Height(verifySectionView) - 4)
	configView := m.configtui.View()

	rightView := lipgloss.JoinVertical(lipgloss.Left, configView, verifySectionView)

	return lipgloss.JoinHorizontal(lipgloss.Top, leftView, rightView)
}
