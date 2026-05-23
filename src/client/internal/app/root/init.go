package root

import (
	tea "charm.land/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
)

func (m *Model) Init() tea.Cmd {
	return tea.Batch(
		m.pages[m.pageOrder[m.currentPage]].Init(),
		tea.RequestBackgroundColor,
		checkBgTickCmd(),
		styles.DetectNerdFontCmd(),
	)
}
