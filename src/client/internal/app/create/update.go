package create

import (
	"charm.land/bubbles/v2/key"
	tea "charm.land/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/config"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

func (m *Model) Update(msg tea.Msg) (app.PageModel, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		if m.LoadSection.Focused() && key.Matches(msg, m.LoadSection.KeyMap().PressButton) &&
			m.LoadSection.Enabled() {
			return m, postListConfigCmd(
				m.listtui.VocabEditor.GetCurrentContent(),
				m.configtui.RawSessionConfig,
				m.serverPort,
			)
		}

	case ListConfigPostedMsg:
		m.LoadSection.ListStatus = StatusLoaded
		m.LoadSection.ConfigStatus = StatusLoaded
	}

	util.UpdaterPtr(&cmds, m.listtui, msg)
	util.UpdaterPtr(&cmds, m.configtui, msg)

	if _, ok := msg.(tea.KeyPressMsg); ok &&
		m.listtui.VocabEditor.IsInsertMode() &&
		m.listtui.VocabEditor.Focused() &&
		m.LoadSection.ListStatus == StatusLoaded && !m.HasOverlay() {
		m.LoadSection.ListStatus = StatusPending
	}

	if m.listtui.VocabEditor.GetCurrentContent() == "" {
		if m.LoadSection.ListStatus == StatusPending {
			m.LoadSection.ListStatus = StatusMissing
		}
	} else {
		if m.LoadSection.ListStatus == StatusMissing {
			m.LoadSection.ListStatus = StatusPending
		}
	}

	if m.configtui.AppStatus == config.CreateSessionConfig {
		// when the user is going through the wizard again there is no config!
		if m.LoadSection.ConfigStatus == StatusPending || m.LoadSection.ConfigStatus == StatusLoaded {
			m.LoadSection.ConfigStatus = StatusMissing
		}
	} else {
		if m.LoadSection.ConfigStatus == StatusMissing {
			m.LoadSection.ConfigStatus = StatusPending
		}
	}

	return m, tea.Batch(cmds...)
}
