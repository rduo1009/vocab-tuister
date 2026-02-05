package util

import tea "charm.land/bubbletea/v2"

func MsgCmd(msg tea.Msg) tea.Cmd {
	return func() tea.Msg {
		return msg
	}
}
