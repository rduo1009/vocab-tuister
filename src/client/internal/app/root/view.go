package root

import (
	"strings"

	tea "github.com/charmbracelet/bubbletea/v2"
)

func (m *Model) View() tea.View {
	var b strings.Builder

	b.WriteString(m.tabs.View())
	b.WriteRune('\n')

	b.WriteString(m.pages[m.pageOrder[m.currentPage]].View())
	if m.tabs.Focused() {
		b.WriteString(m.help.View(m.keys))
	} else {
		b.WriteString(m.help.View(m.pages[m.pageOrder[m.currentPage]].KeyMap()))
	}

	v := tea.NewView(b.String())
	v.AltScreen = true
	v.WindowTitle = "Vocab Tester"
	return v
}
