package session

import (
	tea "charm.land/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

func (m *Model) Init() tea.Cmd {
	if m.appStatus == Initialised {
		return m.questions[m.currentIndex].Init()
	}
	return util.MsgCmd(navigator.AddNavigableMsg{
		Components: []navigator.Navigable{
			m.returnButton,
		},
	})
}
