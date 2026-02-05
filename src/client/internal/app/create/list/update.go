package list

import (
	"charm.land/bubbles/v2/key"
	tea "charm.land/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/dropdown"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

// func saveList(filePath, list string) tea.Cmd {
// 	return func() tea.Msg {
// 		absPath, err := filepath.Abs(filePath)
// 		if err != nil {
// 			return errMsg{err}
// 		}

// 		if err = os.WriteFile(absPath, []byte(list), 0o644); err != nil {
// 			return errMsg{err}
// 		}

// 		return saveMsg(absPath)
// 	}
// }

func (m *Model) Update(msg tea.Msg) (util.ComponentModel, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyMsg:
		if m.HeaderSection.Focused() {
			switch {
			case key.Matches(msg, m.HeaderSection.KeyMap().OpenDropdown):
				cmds = append(cmds, util.MsgCmd(dropdown.DropdownStartMsg{}))
			}
		} else if m.SelectButton.Focused() {
			switch {
			case key.Matches(msg, m.SelectButton.KeyMap().PressButton): // TODO:
			}
		}

		// NOTE: Normal mode cannot be disabled in the editor,
		// so have to manually prevent escaping to normal mode
		if msg.String() != "esc" {
			util.UpdaterPtr(&cmds, m.VocabEditor, msg)
		}
	default:
		util.UpdaterPtr(&cmds, m.VocabEditor, msg)
	}

	return m, tea.Batch(cmds...)
}
