package config

import (
	"github.com/charmbracelet/bubbles/v2/help"
	"github.com/charmbracelet/bubbles/v2/key"
)

type keyMap struct {
	NextFocus   key.Binding
	PressButton key.Binding
	Help        key.Binding
	Quit        key.Binding
}

var headerKeys = keyMap{
	NextFocus: key.NewBinding(
		key.WithKeys("tab"),
		key.WithHelp("tab", "switch focus"),
	),
	PressButton: key.NewBinding(
		key.WithKeys("enter"),
		key.WithHelp("↵", "press button"),
	),
	Quit: key.NewBinding(
		key.WithKeys("ctrl+q", "ctrl+c"),
		key.WithHelp("ctrl+q", "quit"),
	),
}

func (k keyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextFocus, k.PressButton, k.Help, k.Quit}
}

func (k keyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{{k.NextFocus, k.PressButton, k.Help, k.Quit}}
}

func (hb *headerBorder) KeyMap() help.KeyMap {
	return headerKeys
}

type formBorderKeyMap struct {
	fb *formBorder
}

func (k formBorderKeyMap) ShortHelp() []key.Binding {
	return k.fb.form.KeyBinds()
}

func (k formBorderKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{k.fb.form.KeyBinds()}
}

func (fb *formBorder) KeyMap() help.KeyMap {
	return formBorderKeyMap{fb: fb}
}

// KeyMap helps satisfy the StringViewModel interface. It returns the help.KeyMap of the focused component.
//
// It should never be ran in the root model - the KeyMap functions of the subcomponents should be preferred.
func (m *Model) KeyMap() help.KeyMap {
	if m.FormBorder.Focused() {
		return m.FormBorder.KeyMap()
	}

	if m.HeaderBorder.Focused() {
		return m.HeaderBorder.KeyMap()
	}

	panic("unreachable")
}
