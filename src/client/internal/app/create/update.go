package create

import (
	"reflect"
	"strings"

	tea "charm.land/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/dropdown"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/filepicker"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

func (m *Model) Update(msg tea.Msg) (util.PageModel, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg.(type) {
	case filepicker.FilepickStartMsg:
		m.configtuiFilepickerStatus = filepickerActive

	case filepicker.FilepickPickedMsg, filepicker.FilepickExitMsg:
		m.configtuiFilepickerStatus = filepickerInactive

	case dropdown.DropdownStartMsg:
		m.listtuiModeDropdownActive = true

	case dropdown.DropdownPickedMsg, dropdown.DropdownExitMsg:
		m.listtuiModeDropdownActive = false
	}

	if m.configtuiFilepickerStatus == filepickerUninitialised {
		util.UpdaterPtr(&cmds, m.configtuiFilepicker, msg)

		// HACK: Ensure that the filepicker is set up properly
		msgType := reflect.TypeOf(msg)
		if msgType != nil && strings.HasSuffix(msgType.String(), ".readDirMsg") {
			m.configtuiFilepickerStatus = filepickerInactive
		}
	}
	if m.HasOverlay() {
		if m.configtuiFilepickerStatus == filepickerActive {
			util.UpdaterPtr(&cmds, m.configtuiFilepicker, msg)
		} else if m.configtui.HeaderSection.Focused() && m.listtuiModeDropdownActive {
			util.UpdaterPtr(&cmds, m.listtuiModeDropdown, msg)
		}
	} else {
		util.UpdaterPtr(&cmds, m.configtui, msg)
		util.UpdaterPtr(&cmds, m.listtui, msg)
	}

	return m, tea.Batch(cmds...)
}
