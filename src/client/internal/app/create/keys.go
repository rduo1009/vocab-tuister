package create

import (
	"charm.land/bubbles/v2/help"
	"charm.land/bubbles/v2/key"
)

type loadButtonKeyMap struct {
	PressButton   key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k loadButtonKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextFocus, k.PressButton, k.Help, k.Quit}
}

func (k loadButtonKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.PressButton, k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

func (ls *loadSection) KeyMap() loadButtonKeyMap {
	return loadButtonKeyMap{
		PressButton: key.NewBinding(
			key.WithKeys("enter"),
			key.WithHelp("enter", "press button"),
		),
		PreviousFocus: key.NewBinding(
			key.WithKeys("["),
			key.WithHelp("[", "focus previous"),
		),
		NextFocus: key.NewBinding(
			key.WithKeys("]"),
			key.WithHelp("]", "focus next"),
		),
		Help: key.NewBinding(
			key.WithKeys("ctrl+h"),
			key.WithHelp("ctrl+h", "toggle additional help"),
		),
		Quit: key.NewBinding(
			key.WithKeys("ctrl+q", "ctrl+c"),
			key.WithHelp("ctrl+q", "quit"),
		),
	}
}

func (m *Model) KeyMap() help.KeyMap {
	if m.listtui.HeaderSection.Focused() || m.listtui.SelectButton.Focused() ||
		m.listtui.VocabEditor.Focused() {
		return m.listtui.KeyMap()
	}

	if m.listtui.ModeDropdownActive {
		return m.listtui.ModeDropdown.KeyMap()
	}

	if m.configtui.HeaderSection.Focused() || m.configtui.ResetButton.Focused() ||
		m.configtui.FormSection.Focused() {
		return m.configtui.KeyMap()
	}

	if m.configtui.FilepickerActive {
		return m.configtui.Filepicker.KeyMap()
	}

	if m.LoadSection.Focused() {
		return m.LoadSection.KeyMap()
	}

	panic("unreachable")
}
