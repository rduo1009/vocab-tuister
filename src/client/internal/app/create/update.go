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
	case filepicker.FilepickStartMsg:
		switch msg.ID {
		case "configtuiFilepicker":
			m.configtuiFilepickerActive = true
		case "listtuiFilepicker":
			m.listtuiFilepickerActive = true
		}

	case filepicker.FilepickPickedMsg:
		switch msg.ID {
		case "configtuiFilepicker":
			m.configtuiFilepickerActive = false
		case "listtuiFilepicker":
			m.listtuiFilepickerActive = false
		}

	case filepicker.FilepickExitMsg:
		switch msg.ID {
		case "configtuiFilepicker":
			m.configtuiFilepickerActive = false
		case "listtuiFilepicker":
			m.listtuiFilepickerActive = false
		}

	case saveas.SaveAsStartMsg:
		switch msg.ID {
		case "listtuiSaveAs":
			m.listtuiSaveAsActive = true
		}

	case saveas.SaveAsSelectedMsg:
		switch msg.ID {
		case "listtuiSaveAs":
			m.listtuiSaveAsActive = false
		}

	case saveas.SaveAsExitMsg:
		switch msg.ID {
		case "listtuiSaveAs":
			m.listtuiSaveAsActive = false
		}

	case dropdown.DropdownStartMsg:
		m.listtuiModeDropdownActive = true

	case dropdown.DropdownPickedMsg, dropdown.DropdownExitMsg:
		m.listtuiModeDropdownActive = false
	}

	if m.HasOverlay() {
		if m.configtuiFilepickerActive {
			util.UpdaterPtr(&cmds, m.configtuiFilepicker, msg)
		} else if m.listtuiFilepickerActive {
			util.UpdaterPtr(&cmds, m.listtuiFilepicker, msg)
		} else if m.listtuiSaveAsActive {
			util.UpdaterPtr(&cmds, m.listtuiSaveAs, msg)
		} else if m.listtuiModeDropdownActive {
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
