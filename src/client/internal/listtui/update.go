package listtui

import (
	"os"
	"path/filepath"

	"github.com/charmbracelet/bubbles/v2/key"
	tea "github.com/charmbracelet/bubbletea/v2"
)

type (
	errMsg  struct{ err error }
	saveMsg string
)

func saveList(filePath, list string) tea.Cmd {
	return func() tea.Msg {
		absPath, err := filepath.Abs(filePath)
		if err != nil {
			return errMsg{err}
		}

		if err = os.WriteFile(absPath, []byte(list), 0o644); err != nil {
			return errMsg{err}
		}

		return saveMsg(absPath)
	}
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd
	var cmd tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		switch {
		case key.Matches(msg, m.keys.HideCursor):
			if m.textarea.Focused() {
				m.textarea.Blur()
			}

		case key.Matches(msg, m.keys.Quit):
			return m, tea.Quit

		case key.Matches(msg, m.keys.Save):
			return m, saveList(m.filePath, m.textarea.Value())

		case key.Matches(msg, m.keys.Help):
			m.help.ShowAll = !m.help.ShowAll

		default:
			if !m.textarea.Focused() {
				cmd = m.textarea.Focus()
				cmds = append(cmds, cmd)
			}
		}

	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height
		m.help.Width = m.width

	case errMsg:
		m.err = msg.err
		return m, nil

	case saveMsg:
		return m, tea.Quit
	}

	m.textarea, cmd = m.textarea.Update(msg)
	cmds = append(cmds, cmd)

	return m, tea.Batch(cmds...)
}
