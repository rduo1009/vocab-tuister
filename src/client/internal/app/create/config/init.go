package config

import (
	tea "charm.land/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

func (m *Model) Init() tea.Cmd {
	return tea.Batch(
		m.form.Init(),
		util.MsgCmd(
			navigator.AddNavigableMsg{Components: []navigator.Navigable{m.HeaderSection, m.FormSection}},
		),
	)
}
