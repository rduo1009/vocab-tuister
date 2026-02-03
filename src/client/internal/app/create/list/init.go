package list

import (
	tea "github.com/charmbracelet/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

func (m *Model) Init() tea.Cmd {
	return tea.Batch(
		m.VocabEditor.Init(),
		m.VocabEditor.CursorBlink(),
		util.MsgCmd(navigator.AddNavigableMsg{
			Components: []navigator.Navigable{m.HeaderSection, m.VocabEditor, m.SelectButton},
		}),
	)
}
