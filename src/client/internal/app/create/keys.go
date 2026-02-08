package create

import "charm.land/bubbles/v2/help"

func (m *Model) KeyMap() help.KeyMap {
	if m.configtui.HeaderSection.Focused() || m.configtui.ResetButton.Focused() ||
		m.configtui.FormSection.Focused() {
		return m.configtui.KeyMap()
	}

	if m.configtuiFilepickerActive {
		return m.configtuiFilepicker.KeyMap() // XXX: Currently unused? or maybe used?
	}

	if m.listtui.HeaderSection.Focused() || m.listtui.SelectButton.Focused() || m.listtui.VocabEditor.Focused() {
		return m.listtui.KeyMap()
	}

	if m.listtuiModeDropdownActive {
		return m.listtuiModeDropdown.KeyMap()
	}

	panic("unreachable")
}
