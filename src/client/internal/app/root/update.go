package root

import (
	"charm.land/bubbles/v2/key"
	tea "charm.land/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/errordialog"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/types/modes"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

func (m *Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		// Applied to all pages of the TUI
		if key.Matches(msg, m.keys.Quit) {
			return m, tea.Quit
		}

		if m.errorDialog.Visible() {
			util.UpdaterVal(&cmds, &m.errorDialog, msg)
		}

		if !m.pages[m.pageOrder[m.currentPage]].HasOverlay() {
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
				// to re-add the navigable components
				cmds = append(cmds, m.pages[m.pageOrder[m.currentPage]].Init())

			case key.Matches(msg, m.keys.Right):
				if m.currentPage < len(m.pageOrder)-1 {
					m.currentPage++
					m.navigator.Reset()
					m.tabs.Next()
				}
				cmds = append(cmds, m.pages[m.pageOrder[m.currentPage]].Init())
			}
		}

	case tea.WindowSizeMsg:
		m.width, m.height = msg.Width, msg.Height
		m.help.SetWidth(msg.Width)
		m.tabs.Width = msg.Width

	case navigator.AddNavigableMsg:
		m.navigator.Add(msg.Components...)

	case navigator.RemoveNavigableMsg:
		m.navigator.Remove(msg.IDs...)

	case navigator.ReplaceNavigableMsg:
		m.navigator.Replace(msg.ID, msg.Components...)

	case navigator.FocusNavigableMsg:
		if err := m.navigator.FocusNavigable(msg.ID); err != nil {
			return m, util.MsgCmd(app.ErrMsg(err))
		}

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
		return m, m.errorDialog.SetError(msg)

	case errordialog.TimeoutMsg:
		util.UpdaterVal(&cmds, &m.errorDialog, msg)
	}

	util.UpdaterPtr(&cmds, m.pages[m.pageOrder[m.currentPage]], msg)

	return m, tea.Batch(cmds...)
}
