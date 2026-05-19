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
		if m.VerifySection.Focused() && key.Matches(msg, m.VerifySection.KeyMap().PressButton) &&
			m.VerifySection.Enabled() {
			return m, postListConfigCmd(
				m.listtui.VocabEditor.GetCurrentContent(),
				m.configtui.RawSessionConfig,
				m.serverPort,
			)
		}

	case ListConfigPostedMsg:
		m.VerifySection.ListStatus = StatusVerified
		m.VerifySection.ConfigStatus = StatusVerified
	}

	util.UpdaterPtr(&cmds, m.listtui, msg)
	util.UpdaterPtr(&cmds, m.configtui, msg)

	if _, ok := msg.(tea.KeyPressMsg); ok &&
		m.listtui.VocabEditor.IsInsertMode() &&
		m.listtui.VocabEditor.Focused() &&
		m.VerifySection.ListStatus == StatusVerified && !m.HasOverlay() {
		m.VerifySection.ListStatus = StatusPending
	}

	if m.listtui.VocabEditor.GetCurrentContent() == "" {
		if m.VerifySection.ListStatus == StatusPending {
			m.VerifySection.ListStatus = StatusMissing
		}
	} else {
		if m.VerifySection.ListStatus == StatusMissing {
			m.VerifySection.ListStatus = StatusPending
		}
	}

	if m.configtui.AppStatus == config.CreateSessionConfig {
		// when the user is going through the wizard again there is no config!
		if m.VerifySection.ConfigStatus == StatusPending || m.VerifySection.ConfigStatus == StatusVerified {
			m.VerifySection.ConfigStatus = StatusMissing
		}
	} else {
		if m.VerifySection.ConfigStatus == StatusMissing {
			m.VerifySection.ConfigStatus = StatusPending
		}
	}

	return m, tea.Batch(cmds...)
}
