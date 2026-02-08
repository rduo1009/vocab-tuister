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
	return m.configtuiFilepickerActive || m.listtuiFilepickerActive || m.listtuiSaveAsActive ||
		m.listtuiModeDropdownActive
}

func (m *Model) OverlayView(width, height int) (view string, x, y int) {
	if m.configtuiFilepickerActive {
		m.configtuiFilepicker.SetWidth(width / 2)
		m.configtuiFilepicker.SetHeight(height / 2)
		return m.configtuiFilepicker.View(width, height)
	} else if m.listtuiFilepickerActive {
		m.listtuiFilepicker.SetWidth(width / 2)
		m.listtuiFilepicker.SetHeight(height / 2)
		return m.listtuiFilepicker.View(width, height)
	} else if m.listtuiSaveAsActive {
		m.listtuiSaveAs.SetWidth(width / 2)
		m.listtuiSaveAs.SetHeight(height / 2)
		return m.listtuiSaveAs.View(width, height)
	} else if m.listtuiModeDropdownActive {
		view = m.listtuiModeDropdown.View()
		x = 12
		y = 4
		return view, x, y
	}
	panic("unreachable")
}

func (m *Model) View() string {
	return lipgloss.JoinHorizontal(lipgloss.Top, m.listtui.View(), m.configtui.View())
}
