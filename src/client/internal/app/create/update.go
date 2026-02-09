package create

import (
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
		m.listtuiModeDropdownActive = true

	case dropdown.PickedMsg, dropdown.ExitMsg:
		m.listtuiModeDropdownActive = false
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
		if _, ok := msg.(tea.KeyMsg); !ok {
			util.UpdaterPtr(&cmds, m.configtuiFilepicker, msg)
			util.UpdaterPtr(&cmds, m.listtuiFilepicker, msg)
			util.UpdaterPtr(&cmds, m.listtuiSaveAs, msg)
		}

		util.UpdaterPtr(&cmds, m.configtui, msg)
		util.UpdaterPtr(&cmds, m.listtui, msg)
	}

	return m, tea.Batch(cmds...)
}
