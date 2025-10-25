package create

import (
	tea "github.com/charmbracelet/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/config"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

func (m *Model) Update(msg tea.Msg) (util.ComponentModel, tea.Cmd) {
	var cmds []tea.Cmd
	// var cmd tea.Cmd

	// switch msg := msg.(type) {
	// }

	if m.configtui.HeaderSection.Focused() || m.configtui.FormSection.Focused() || m.configtui.ResetButton.Focused() {
		configtui, cmd := m.configtui.Update(msg)
		m.configtui = configtui.(*config.Model)
		cmds = append(cmds, cmd)
	}

	return m, tea.Batch(cmds...)
}
