package list

import (
	"github.com/charmbracelet/bubbles/v2/key"
	tea "github.com/charmbracelet/bubbletea/v2"

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
			//if m.statusDropdownActive {
			//	switch {
			//	case key.Matches(msg, m.HeaderSection.KeyMap().PreviousFocus):
			//		m.statusDropdownActive = false
			//	case key.Matches(msg, m.HeaderSection.KeyMap().NextFocus):
			//		m.statusDropdownActive = false
			//	}
			//} else {
			switch {
			case key.Matches(msg, m.HeaderSection.KeyMap().OpenDropdown):
				cmds = append(cmds, util.MsgCmd(dropdown.DropdownStartMsg{}))
			}
		} else if m.SelectButton.Focused() {
			switch {
			case key.Matches(msg, m.SelectButton.KeyMap().PressButton): // TODO:
			}
		}
	}

	_, cmd := m.VocabEditor.Update(msg)
	cmds = append(cmds, cmd)

	return m, tea.Batch(cmds...)
}
