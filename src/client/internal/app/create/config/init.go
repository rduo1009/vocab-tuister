package config

import (
	tea "github.com/charmbracelet/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
)

func (m *Model) Init() tea.Cmd {
	return tea.Batch(m.form.Init(), func() tea.Msg {
		return navigator.AddNavigableMsg{
			Components: []navigator.Navigable{m.HeaderSection, m.FormSection},
		}
	})
}
