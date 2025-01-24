package sessiontui

import "github.com/charmbracelet/bubbles/v2/key"

type KeyMap struct {
	NextOption key.Binding
	Up         key.Binding
	Down       key.Binding
	Submit     key.Binding
	Help       key.Binding
	Quit       key.Binding
}

var DefaultKeyMap = KeyMap{
	NextOption: key.NewBinding(
		key.WithKeys("tab"),
		key.WithHelp("tab", "next option"),
	),
	Up: key.NewBinding(
		key.WithKeys("up"),
		key.WithHelp("↑", "move up"),
	),
	Down: key.NewBinding(
		key.WithKeys("down"),
		key.WithHelp("↓", "move down"),
	),
	Submit: key.NewBinding(
		key.WithKeys("enter"),
		key.WithHelp("⏎", "submit answer"),
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

func (k KeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextOption, k.Submit, k.Help, k.Quit}
}

func (k KeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.NextOption, k.Up, k.Down, k.Submit},
		{k.Help, k.Quit},
	}
}
