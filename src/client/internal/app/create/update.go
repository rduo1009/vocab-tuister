package create

import (
	"reflect"
	"strings"

	tea "github.com/charmbracelet/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/filepicker"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

func (m *Model) Update(msg tea.Msg) (util.PageModel, tea.Cmd) {
	var cmds []tea.Cmd

	if _, ok := msg.(filepicker.FilepickStartMsg); ok {
		m.configtuiFilepickerStatus = filepickerActive
	} else if _, ok := msg.(filepicker.FilepickPickedMsg); ok {
		m.configtuiFilepickerStatus = filepickerInactive
	} else if _, ok := msg.(filepicker.FilepickExitMsg); ok {
		m.configtuiFilepickerStatus = filepickerInactive
	}

	if m.configtuiFilepickerStatus == filepickerUninitialised {
		_, cmd := m.configtuiFilepicker.Update(msg)

		// Ensure that the filepicker is set up properly
		msgType := reflect.TypeOf(msg)
		if msgType != nil && strings.HasSuffix(msgType.String(), ".readDirMsg") {
			m.configtuiFilepickerStatus = filepickerInactive
		}

		cmds = append(cmds, cmd)
	}
	if m.HasOverlay() {
		if m.configtuiFilepickerStatus == filepickerActive {
			_, cmd := m.configtuiFilepicker.Update(msg)
			cmds = append(cmds, cmd)
		}
	} else {
		if m.configtui.HeaderSection.Focused() || m.configtui.FormSection.Focused() || m.configtui.ResetButton.Focused() {
			_, cmd := m.configtui.Update(msg)
			cmds = append(cmds, cmd)
		}
	}

	return m, tea.Batch(cmds...)
}
