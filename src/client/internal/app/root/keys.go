package root

import (
	"charm.land/bubbles/v2/key"
)

type keyMap struct {
	Left          key.Binding
	Right         key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Submit        key.Binding
	Help          key.Binding
	Quit          key.Binding
}

var keys = keyMap{
	Left: key.NewBinding(
		key.WithKeys("left"),
		key.WithHelp("←", "left tab"),
	),
	Right: key.NewBinding(
		key.WithKeys("right"),
		key.WithHelp("→", "right tab"),
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

func (k keyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextFocus, k.Left, k.Right, k.Help, k.Quit}
}

func (k keyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.Left, k.Right, k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}
