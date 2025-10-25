package root

import (
	"github.com/charmbracelet/bubbles/v2/key"
)

type keyMap struct {
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Left          key.Binding
	Right         key.Binding
	Submit        key.Binding
	Help          key.Binding
	Quit          key.Binding
}

var keys = keyMap{
	PreviousFocus: key.NewBinding(
		key.WithKeys("["),
		key.WithHelp("[", "focus previous"),
	),
	NextFocus: key.NewBinding(
		key.WithKeys("]"),
		key.WithHelp("]", "focus next"),
	),
	Left: key.NewBinding(
		key.WithKeys("left"),
		key.WithHelp("↑", "left tab"),
	),
	Right: key.NewBinding(
		key.WithKeys("right"),
		key.WithHelp("→", "right tab"),
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
	return []key.Binding{k.NextFocus, k.Help, k.Quit}
}

func (k keyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.PreviousFocus, k.NextFocus, k.Left, k.Right},
		{k.Help, k.Quit},
	}
}
