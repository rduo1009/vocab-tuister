package config

import (
	tea "charm.land/bubbletea/v2"
)

func (m *Model) Init() tea.Cmd {
	return tea.Batch(
		m.form.Init(),
		m.Filepicker.Init(),
	)
}
