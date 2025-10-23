package create

func (m *Model) SetWidth(width int) {
	m.width = width
	m.configtui.SetWidth(width)
}

func (m *Model) SetHeight(height int) {
	m.height = height
	m.configtui.SetHeight(height)
}

func (m *Model) View() string {
	return m.configtui.View()
}
