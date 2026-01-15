package util

import tea "github.com/charmbracelet/bubbletea/v2"

func MsgCmd(msg tea.Msg) tea.Cmd {
	return func() tea.Msg {
		return msg
	}
}
