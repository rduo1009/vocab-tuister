package create

import (
	"charm.land/bubbles/v2/key"
	tea "charm.land/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/dropdown"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/filepicker"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/saveas"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

func (m *Model) Update(msg tea.Msg) (app.PageModel, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		if m.LoadSection.Focused() && key.Matches(msg, m.LoadSection.KeyMap().PressButton) &&
			m.LoadSection.Enabled() {
			cmds = append(cmds, postListConfigCmd(
				m.listtui.VocabEditor.GetCurrentContent(),
				m.configtui.RawSessionConfig,
				5500, // TODO: actual server port here
			))
		}

	case ListConfigPostedMsg:
		m.LoadSection.ListStatus = StatusLoaded
		m.LoadSection.ConfigStatus = StatusLoaded

	case filepicker.StartMsg:
		switch msg.ID {
		case "configtuiFilepicker":
			m.configtuiFilepickerActive = true

		case "listtuiFilepicker":
			m.listtuiFilepickerActive = true
		}

	case filepicker.PickedMsg:
		switch msg.ID {
		case "configtuiFilepicker":
			m.configtuiFilepickerActive = false

		case "listtuiFilepicker":
			m.listtuiFilepickerActive = false
		}

	case filepicker.ExitMsg:
		switch msg.ID {
		case "configtuiFilepicker":
			m.configtuiFilepickerActive = false

		case "listtuiFilepicker":
			m.listtuiFilepickerActive = false
		}

	case saveas.StartMsg:
		if msg.ID == "listtuiSaveAs" {
			m.listtuiSaveAsActive = true
		}

	case saveas.SelectedMsg:
		if msg.ID == "listtuiSaveAs" {
			m.listtuiSaveAsActive = false
		}

	case saveas.ExitMsg:
		if msg.ID == "listtuiSaveAs" {
			m.listtuiSaveAsActive = false
		}

	case dropdown.StartMsg:
		if msg.ID == "listtuiDropdown" {
			m.listtuiModeDropdownActive = true
		}

	case dropdown.PickedMsg:
		if msg.ID == "listtuiDropdown" {
			m.listtuiModeDropdownActive = false
		}

	case dropdown.ExitMsg:
		if msg.ID == "listtuiDropdown" {
			m.listtuiModeDropdownActive = false
		}
	}

	if m.HasOverlay() {
		switch {
		case m.configtuiFilepickerActive:
			util.UpdaterPtr(&cmds, m.configtuiFilepicker, msg)

		case m.listtuiFilepickerActive:
			util.UpdaterPtr(&cmds, m.listtuiFilepicker, msg)

		case m.listtuiSaveAsActive:
			util.UpdaterPtr(&cmds, m.listtuiSaveAs, msg)

		case m.listtuiModeDropdownActive:
			util.UpdaterPtr(&cmds, m.listtuiModeDropdown, msg)
		}
	} else {
		if _, ok := msg.(tea.KeyPressMsg); !ok {
			util.UpdaterPtr(&cmds, m.configtuiFilepicker, msg)
			util.UpdaterPtr(&cmds, m.listtuiFilepicker, msg)
			util.UpdaterPtr(&cmds, m.listtuiSaveAs, msg)
		}

		if _, ok := msg.(tea.KeyPressMsg); ok &&
			m.listtui.VocabEditor.IsInsertMode() &&
			m.listtui.VocabEditor.Focused() &&
			m.LoadSection.ListStatus == StatusLoaded {
			m.LoadSection.ListStatus = StatusPending
		}

		util.UpdaterPtr(&cmds, m.configtui, msg)
		util.UpdaterPtr(&cmds, m.listtui, msg)
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

	if m.configtui.RawSessionConfig == "" {
		if m.LoadSection.ConfigStatus == StatusPending {
			m.LoadSection.ConfigStatus = StatusMissing
		}
	} else {
		if m.LoadSection.ConfigStatus == StatusMissing {
			m.LoadSection.ConfigStatus = StatusPending
		}
	}

	return m, tea.Batch(cmds...)
}
