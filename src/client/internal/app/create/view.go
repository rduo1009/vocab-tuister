package create

import "charm.land/lipgloss/v2"

func (m *Model) SetWidth(width int) {
	m.width = width
	m.configtui.SetWidth(width / 2)
	m.listtui.SetWidth(width / 2)
}

func (m *Model) SetHeight(height int) {
	m.height = height
	m.configtui.SetHeight(height)
	m.listtui.SetHeight(height)
}

func (m *Model) HasOverlay() bool {
	return m.configtuiFilepickerStatus == filepickerActive
}

func (m *Model) OverlayView(width, height int) string {
	if m.configtuiFilepickerStatus == filepickerActive {
		m.configtuiFilepicker.Width = width
		m.configtuiFilepicker.Height = height
		return m.configtuiFilepicker.View()
	}
	panic("unreachable")
}

func (m *Model) View() string {
	return lipgloss.JoinHorizontal(lipgloss.Top, m.listtui.View(), m.configtui.View())
}
