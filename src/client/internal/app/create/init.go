package create

import (
	tea "charm.land/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/config"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

func (m *Model) Init() tea.Cmd {
	components := []navigator.Navigable{
		m.listtui.HeaderSection,
		m.listtui.VocabEditor,
		m.listtui.SelectButton,
	}
	if m.configtui.AppStatus == config.CreateSessionConfig {
		components = append(components,
			m.configtui.HeaderSection,
			m.configtui.FormSection,
		)
	} else { // m.configtui.AppStatus == config.ReviewSessionConfig
		components = append(components,
			m.configtui.HeaderSection,
			m.configtui.ResetButton,
			m.configtui.FormSection,
		)
	}

	components = append(components, m.LoadSection)

	return tea.Batch(
		util.MsgCmd(navigator.AddNavigableMsg{Components: components}),
		m.listtui.Init(),
		m.configtui.Init(),
		m.listtuiModeDropdown.Init(),
		m.listtuiFilepicker.Init(),
		m.listtuiSaveAs.Init(),
		m.configtuiFilepicker.Init(),
	)
}
