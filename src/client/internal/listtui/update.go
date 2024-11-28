package listtui

import (
	"os"
	"path/filepath"

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

		file, err := os.Create(absPath)
		if err != nil {
			return errMsg{err}
		}

		if _, err = file.WriteString(list); err != nil {
			return errMsg{err}
		}

		return saveMsg(filePath)
	}
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd
	var cmd tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		switch msg.String() {
		case "esc":
			if m.textarea.Focused() {
				m.textarea.Blur()
			}
		case "ctrl+c":
			return m, tea.Quit

		case "ctrl+s":
			return m, saveList(m.filePath, m.textarea.Value())

		default:
			if !m.textarea.Focused() {
				cmd = m.textarea.Focus()
				cmds = append(cmds, cmd)
			}
		}

	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height

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
