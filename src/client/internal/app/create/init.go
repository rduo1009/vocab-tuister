package create

import (
	tea "charm.land/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

func (m *Model) Init() tea.Cmd {
	return tea.Batch(
		tea.Sequence(
			util.MsgCmd(navigator.AddNavigableMsg{
				Components: []navigator.Navigable{
					m.listtui.HeaderSection,
					m.listtui.VocabEditor,
					m.listtui.SelectButton,
				},
			}),
			util.MsgCmd(navigator.AddNavigableMsg{
				Components: []navigator.Navigable{
					m.configtui.HeaderSection,
					m.configtui.FormSection,
				},
			}),
		),
		m.listtui.Init(),
		m.configtui.Init(),
		m.listtuiModeDropdown.Init(),
		m.listtuiFilepicker.Init(),
		m.configtuiFilepicker.Init(),
	)
}
