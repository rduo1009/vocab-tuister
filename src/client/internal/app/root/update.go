package root

import (
	"time"

	"charm.land/bubbles/v2/key"
	tea "charm.land/bubbletea/v2"
	chromastyles "github.com/alecthomas/chroma/v2/styles"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/errordialog"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/tabs"
	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type checkBgTickMsg time.Time

func checkBgTickCmd() tea.Cmd {
	return tea.Tick(time.Millisecond*500, func(t time.Time) tea.Msg {
		return checkBgTickMsg(t)
	})
}

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
				util.UpdaterPtr(&cmds, m.pages[m.pageOrder[m.currentPage]], nil)
				return m, tea.Batch(cmds...)

			case key.Matches(msg, m.keys.NextFocus):
				m.navigator.Next()
				util.UpdaterPtr(&cmds, m.pages[m.pageOrder[m.currentPage]], nil)
				return m, tea.Batch(cmds...)
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
				return m, m.pages[m.pageOrder[m.currentPage]].Init()

			case key.Matches(msg, m.keys.Right):
				if m.currentPage < len(m.pageOrder)-1 {
					m.currentPage++
					m.navigator.Reset()
					m.tabs.Next()
				}

				return m, m.pages[m.pageOrder[m.currentPage]].Init()
			}
		}

	case tea.WindowSizeMsg:
		m.width, m.height = msg.Width, msg.Height
		m.help.SetWidth(msg.Width)
		m.tabs.Width = msg.Width

	case tea.BackgroundColorMsg:
		if msg.IsDark() != m.isDark {
			m.isDark = msg.IsDark()
			m.themes = styles.DefaultThemes(msg.IsDark())
			m.styles.Styles = styles.DefaultStyles(
				m.themes.Current(),
				m.pages[m.pageOrder[m.currentPage]].HasOverlay(),
			)
			chromastyles.Register(m.styles.Editor.Chroma)
			cmds = append(cmds, util.MsgCmd(app.RefreshStylesMsg{}))
		}

	case checkBgTickMsg:
		return m, tea.Batch(
			tea.RequestBackgroundColor,
			checkBgTickCmd(),
		)

	case tabs.SelectTabMsg:
		m.currentPage = msg.Index
		m.navigator.Reset()
		m.tabs.Select(msg.Index)

		if err := m.navigator.FocusNavigable(m.tabs); err != nil {
			return m, util.MsgCmd(app.ErrMsg(err))
		}

		return m, m.pages[m.pageOrder[m.currentPage]].Init()

	case navigator.AddNavigableMsg:
		m.navigator.Add(msg.Components...)

	case navigator.RemoveNavigableMsg:
		if err := m.navigator.Remove(msg.Components...); err != nil {
			return m, util.MsgCmd(app.ErrMsg(err))
		}

	case navigator.ReplaceNavigableMsg:
		if err := m.navigator.Replace(msg.Target, msg.Replacement...); err != nil {
			return m, util.MsgCmd(app.ErrMsg(err))
		}

	case navigator.FocusNavigableMsg:
		if err := m.navigator.FocusNavigable(msg.Target); err != nil {
			return m, util.MsgCmd(app.ErrMsg(err))
		}

	case create.ListConfigPostedMsg:
		m.vocabList = msg.VocabList
		m.sessionConfig = msg.SessionConfig
		m.numberOfQuestions = msg.NumberOfQuestions

	case app.ErrMsg:
		m.err = msg
		return m, m.errorDialog.SetError(msg)

	case errordialog.TimeoutMsg:
		util.UpdaterVal(&cmds, &m.errorDialog, msg)
	}

	util.UpdaterPtr(&cmds, m.pages[m.pageOrder[m.currentPage]], msg)

	if m.pages[m.pageOrder[m.currentPage]].HasOverlay() && !m.overlayExpectedActive {
		m.overlayExpectedActive = true
		m.styles.Styles = styles.DefaultStyles(m.themes.Current(), true)
		chromastyles.Register(m.styles.Editor.Chroma)
		cmds = append(cmds, util.MsgCmd(app.RefreshStylesMsg{}))
	} else if !m.pages[m.pageOrder[m.currentPage]].HasOverlay() && m.overlayExpectedActive {
		m.overlayExpectedActive = false
		m.styles.Styles = styles.DefaultStyles(m.themes.Current(), false)
		chromastyles.Register(m.styles.Editor.Chroma)
		cmds = append(cmds, util.MsgCmd(app.RefreshStylesMsg{}))
	}

	return m, tea.Batch(cmds...)
}
