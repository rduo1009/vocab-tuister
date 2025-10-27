package create

import "github.com/charmbracelet/bubbles/v2/help"

func (m *Model) OverlayKeyMap() help.KeyMap {
	if m.configtuiFilepickerStatus == filepickerActive {
		return m.configtuiFilepicker.KeyMap()
	}
	panic("unreachable")
}

func (m *Model) KeyMap() help.KeyMap {
	if m.configtui.HeaderSection.Focused() || m.configtui.ResetButton.Focused() || m.configtui.FormSection.Focused() {
		return m.configtui.KeyMap()
	}

	panic("not implemented")
}
