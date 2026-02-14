package root

import (
	"charm.land/bubbles/v2/key"
	tea "charm.land/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/types/modes"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

func (m *Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd

	currentPageModel := m.pages[m.pageOrder[m.currentPage]]

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		// Applied to all pages of the TUI
		if key.Matches(msg, m.keys.Quit) {
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
		} else if key.Matches(msg, m.keys.Help) {
			m.overlayHelp.ShowAll = !m.overlayHelp.ShowAll
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
		m.help.SetWidth(msg.Width)
		m.tabs.Width = msg.Width

	case navigator.AddNavigableMsg:
		for _, component := range msg.Components {
			m.navigator.Add(component)
		}

	case navigator.RemoveNavigableMsg:
		for _, id := range msg.IDs {
			m.navigator.Remove(id)
		}

	case navigator.ReplaceNavigableMsg:
		m.navigator.Replace(msg.ID, msg.Components...)

	case create.LoadDataReqMsg:
		cmds = append(
			cmds,
			loadDataCmd(msg.VocabList, msg.RawSessionConfig, 5500), // TODO: actual server port here
		)

	case ListConfigLoadedMsg:
		m.vocabList = msg.vocabList
		m.sessionConfig = msg.sessionConfig
		// XXX: Perhaps a better solution to this whole thing could be done to avoid needing to do this.
		m.pages[modes.Create].(*create.Model).LoadSection.ListStatus = create.StatusLoaded
		m.pages[modes.Create].(*create.Model).LoadSection.ConfigStatus = create.StatusLoaded

	case app.ErrMsg:
		m.err = msg
		return m, tea.Quit
	}

	util.UpdaterPtr(&cmds, currentPageModel, msg)

	return m, tea.Batch(cmds...)
}
