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

	if m.ModeDropdownActive {
		switch msg := msg.(type) {
		case dropdown.PickedMsg:
			if msg.ID != modeDropdownID {
				break
			}

			m.ModeDropdownActive = false

			m.AppStatus = msg.ChosenItem.(createListStatus)
			switch m.AppStatus {
			case InbuiltList:
				m.VocabEditor.SetNormalMode()
				m.VocabEditor.DisableInsertMode(true)
				cmds = append(cmds, util.MsgCmd(filepicker.SetPathMsg{
					ID:   filepickerID,
					Path: m.inbuiltListDir,
				}))

			case LocalList:
				m.VocabEditor.SetNormalMode()
				m.VocabEditor.DisableInsertMode(true)

				homeDir, _ := os.UserHomeDir()
				cmds = append(cmds, util.MsgCmd(filepicker.SetPathMsg{
					ID:   filepickerID,
					Path: homeDir,
				}))

			case CustomList:
				m.VocabEditor.DisableInsertMode(false)
				m.VocabEditor.SetInsertMode()
			}

		case dropdown.ExitMsg:
			if msg.ID == modeDropdownID {
				m.ModeDropdownActive = false
			}
		}

		util.UpdaterPtr(&cmds, m.ModeDropdown, msg)

		return m, tea.Batch(cmds...)
	}

	if m.FilepickerActive {
		switch msg := msg.(type) {
		case filepicker.PickedMsg:
			if msg.ID == filepickerID {
				m.FilepickerActive = false

				cmds = append(cmds, readVocabList(msg.SelectedFile))
			}

		case filepicker.ExitMsg:
			if msg.ID == filepickerID {
				m.FilepickerActive = false
			}
		}

		util.UpdaterPtr(&cmds, m.Filepicker, msg)

		return m, tea.Batch(cmds...)
	}

	if m.SaveAsActive {
		switch msg := msg.(type) {
		case saveas.SelectedMsg:
			if msg.ID == saveAsID {
				m.SaveAsActive = false
				cmds = append(cmds, saveVocabList(msg.Path, m.VocabEditor.GetCurrentContent()))
				cmds = append(cmds, m.SaveAs.RefreshFilepickerDir())
			}

		case saveas.ExitMsg:
			if msg.ID == saveAsID {
				m.SaveAsActive = false
			}
		}

		util.UpdaterPtr(&cmds, m.SaveAs, msg)

		return m, tea.Batch(cmds...)
	}

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		if m.HeaderSection.Focused() {
			if key.Matches(msg, m.HeaderSection.KeyMap().OpenDropdown) {
				m.ModeDropdownActive = true
				return m, nil
			}
		} else if m.SelectButton.Focused() {
			if key.Matches(msg, m.SelectButton.KeyMap().PressButton) {
				switch m.AppStatus {
				case InbuiltList, LocalList:
					m.FilepickerActive = true
					return m, nil

				case CustomList:
					m.SaveAsActive = true
					return m, nil
				}
			}
		}

		// NOTE: Normal mode cannot be disabled in the editor,
		// so have to manually prevent escaping to normal mode
		if msg.String() == "esc" {
			return m, tea.Batch(cmds...)
		}

	case vocabListReadMsg:
		m.VocabEditor.SetContent(string(msg))

	default:
		util.UpdaterPtr(&cmds, m.Filepicker, msg)
		util.UpdaterPtr(&cmds, m.SaveAs, msg)
	}

	util.UpdaterPtr(&cmds, m.VocabEditor, msg)

	return m, tea.Batch(cmds...)
}
