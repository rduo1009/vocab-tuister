package list

import (
	tea "charm.land/bubbletea/v2"
)

func (m *Model) Init() tea.Cmd {
	return tea.Batch(
		m.VocabEditor.Init(),
		m.VocabEditor.CursorBlink(),
		m.ModeDropdown.Init(),
		m.Filepicker.Init(),
		m.SaveAs.Init(),
	)
}
