package create

import (
	tea "github.com/charmbracelet/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

func (m *Model) Update(msg tea.Msg) (util.ComponentModel, tea.Cmd) {
	var cmds []tea.Cmd
	// var cmd tea.Cmd

	// switch msg := msg.(type) {
	// }

	if m.configtui.HeaderBorder.Focused() || m.configtui.FormBorder.Focused() {
		_, cmd := m.configtui.Update(msg)
		cmds = append(cmds, cmd)
	}

	return m, tea.Batch(cmds...)
}
