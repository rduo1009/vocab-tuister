package create

import tea "charm.land/bubbletea/v2"

func (m *Model) Init() tea.Cmd {
	return tea.Batch(
		m.configtui.Init(),
		m.configtuiFilepicker.Init(),
		m.listtui.Init(),
		m.listtuiModeDropdown.Init(),
	)
}
