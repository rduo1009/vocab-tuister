package root

import (
	"github.com/charmbracelet/bubbles/v2/key"
	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/types/modes"
)

func (m *Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd
	var cmd tea.Cmd

	currentPageModel := m.pages[m.pageOrder[m.currentPage]]

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		// Applied to all pages of the TUI
		switch {
		case key.Matches(msg, m.keys.Quit):
			return m, tea.Quit
		case key.Matches(msg, m.keys.Help):
			m.help.ShowAll = !m.help.ShowAll
		case key.Matches(msg, m.keys.NextFocus):
			m.navigator.Next()
		}

		// Applied to only when tabs are selected
		if m.tabs.Focused() {
			switch {
			case key.Matches(msg, m.keys.Left):
				if m.currentPage > 0 {
					m.currentPage--
					m.tabs.Prev()
				}
			case key.Matches(msg, m.keys.Right):
				if m.currentPage < len(m.pageOrder)-1 {
					m.currentPage++
					m.tabs.Next()
				}
			}
		}
	case tea.WindowSizeMsg:
		m.width, m.height = msg.Width, msg.Height
		m.help.Width = msg.Width
		m.tabs.Width = msg.Width

		if m.pageOrder[m.currentPage] == modes.Create {
			currentPageModel.SetWidth(m.width)
			currentPageModel.SetHeight(m.height - lipgloss.Height(m.tabs.View()))
		}
	}

	_, cmd = currentPageModel.Update(msg)
	cmds = append(cmds, cmd)

	return m, tea.Batch(cmds...)
}
