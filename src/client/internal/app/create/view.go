package create

import "github.com/charmbracelet/lipgloss/v2"

func (m *Model) SetWidth(width int) {
	m.width = width
	m.configtui.SetWidth(width)
}

func (m *Model) SetHeight(height int) {
	m.height = height
	m.configtui.SetHeight(height)
}

func (m *Model) HasOverlay() bool {
	return m.configtuiFilepickerStatus == filepickerActive
}

func (m *Model) OverlayView(width, height int) string {
	m.configtuiFilepicker.Width = width
	m.configtuiFilepicker.Height = height
	if m.configtuiFilepickerStatus == filepickerActive {
		return m.configtuiFilepicker.View()
	}
	panic("unreachable")
}

func (m *Model) View() string {
	return lipgloss.JoinHorizontal(lipgloss.Top, m.listtui.View(), m.configtui.View())
}
