package root

import (
	"github.com/charmbracelet/bubbles/v2/key"
	tea "github.com/charmbracelet/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
)

func (m *Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd
	var cmd tea.Cmd

	currentPageModel := m.pages[m.pageOrder[m.currentPage]]

	switch msg := msg.(type) {
	case tea.KeyMsg:
		// Applied to all pages of the TUI
		switch {
		case key.Matches(msg, m.keys.Quit):
			return m, tea.Quit
		}

		if !currentPageModel.HasOverlay() {
			switch {
			case key.Matches(msg, m.keys.Help):
				m.help.ShowAll = !m.help.ShowAll
			case key.Matches(msg, m.keys.PreviousFocus):
				m.navigator.Previous()
			case key.Matches(msg, m.keys.NextFocus):
				m.navigator.Next()
			}
		} else {
			switch {
			case key.Matches(msg, m.keys.Help):
				m.overlayHelp.ShowAll = !m.overlayHelp.ShowAll
			}
		}

		// Applied to only when tabs are selected
		if m.tabs.Focused() {
			switch {
			case key.Matches(msg, m.keys.Left):
				if m.currentPage > 0 {
					m.currentPage--
					m.navigator.Reset()
					m.tabs.Prev()
				}
			case key.Matches(msg, m.keys.Right):
				if m.currentPage < len(m.pageOrder)-1 {
					m.currentPage++
					m.navigator.Reset()
					m.tabs.Next()
				}
			}
		}

	case tea.WindowSizeMsg:
		m.width, m.height = msg.Width, msg.Height
		m.help.Width = msg.Width
		m.tabs.Width = msg.Width

	case navigator.AddNavigableMsg:
		for _, component := range msg.Components {
			m.navigator.Add(component)
		}

	case navigator.RemoveNavigableMsg:
		for _, id := range msg.IDs {
			m.navigator.Remove(id)
		}

	case app.ErrMsg:
		m.err = msg
		return m, tea.Quit
	}

	currentPageModel, cmd = currentPageModel.Update(msg)
	cmds = append(cmds, cmd)

	return m, tea.Batch(cmds...)
}
