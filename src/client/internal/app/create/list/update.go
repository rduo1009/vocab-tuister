package list

import (
	"fmt"
	"os"

	"charm.land/bubbles/v2/key"
	tea "charm.land/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/dropdown"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/filepicker"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/saveas"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

func saveVocabList(filePath, list string) tea.Cmd {
	return func() tea.Msg {
		if err := os.WriteFile(filePath, []byte(list), 0o644); err != nil {
			return app.ErrMsg(fmt.Errorf("failed to save vocab list to %s: %w", filePath, err))
		}
		return nil
	}
}

type vocabListReadMsg string

func readVocabList(filePath string) tea.Cmd {
	return func() tea.Msg {
		b, err := os.ReadFile(filePath)
		if err != nil {
			return app.ErrMsg(fmt.Errorf("failed to read vocab list from %s: %w", filePath, err))
		}

		return vocabListReadMsg(string(b))
	}
}

func (m *Model) Update(msg tea.Msg) (app.ComponentModel, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyMsg:
		if m.HeaderSection.Focused() {
			if key.Matches(msg, m.HeaderSection.KeyMap().OpenDropdown) {
				cmds = append(cmds, util.MsgCmd(dropdown.DropdownStartMsg{}))
			}
		} else if m.SelectButton.Focused() {
			if key.Matches(msg, m.SelectButton.KeyMap().PressButton) {
				switch m.appStatus {
				case InbuiltList, LocalList:
					cmds = append(
						cmds,
						util.MsgCmd(filepicker.FilepickStartMsg{ID: "listtuiFilepicker"}),
					)
				case CustomList:
					cmds = append(
						cmds,
						util.MsgCmd(saveas.SaveAsStartMsg{ID: "listtuiSaveAs"}),
					)
				}
			}
		}

		// NOTE: Normal mode cannot be disabled in the editor,
		// so have to manually prevent escaping to normal mode
		if msg.String() == "esc" {
			// XXX: Maybe returning early will not work anymore as things get added!
			return m, tea.Batch(cmds...)
		}

	case dropdown.DropdownPickedMsg:
		m.appStatus = msg.ChosenItem.(createListStatus)
		switch m.appStatus {
		case InbuiltList:
			m.VocabEditor.SetNormalMode()
			m.VocabEditor.DisableInsertMode(true)
			cmds = append(cmds, util.MsgCmd(
				filepicker.FilepickSetPathMsg{
					ID:   "listtuiFilepicker",
					Path: m.inbuiltListDir,
				},
			))
		case LocalList:
			m.VocabEditor.SetNormalMode()
			m.VocabEditor.DisableInsertMode(true)
			homeDir, _ := os.UserHomeDir()
			cmds = append(cmds, util.MsgCmd(
				filepicker.FilepickSetPathMsg{
					ID:   "listtuiFilepicker",
					Path: homeDir,
				},
			))
		case CustomList:
			m.VocabEditor.DisableInsertMode(false)
			m.VocabEditor.SetInsertMode()
		}

	case vocabListReadMsg:
		m.VocabEditor.SetContent(string(msg))

	case filepicker.FilepickPickedMsg:
		if msg.ID == "listtuiFilepicker" {
			cmds = append(cmds, readVocabList(msg.SelectedFile))
		}

	case saveas.SaveAsSelectedMsg:
		if msg.ID == "listtuiSaveAs" {
			cmds = append(cmds, saveVocabList(msg.Path, m.VocabEditor.GetCurrentContent()))
		}
	}

	util.UpdaterPtr(&cmds, m.VocabEditor, msg)

	return m, tea.Batch(cmds...)
}
