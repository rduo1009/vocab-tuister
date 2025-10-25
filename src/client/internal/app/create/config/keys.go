package config

import (
	"github.com/charmbracelet/bubbles/v2/help"
	"github.com/charmbracelet/bubbles/v2/key"
)

type headerBorderKeyMap struct {
	PreviousFocus key.Binding
	NextFocus     key.Binding
	PressButton   key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k headerBorderKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextFocus, k.PressButton, k.Help, k.Quit}
}

func (k headerBorderKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{{k.NextFocus, k.PressButton, k.Help, k.Quit}}
}

func (hb *headerBorder) KeyMap() help.KeyMap {
	return headerBorderKeyMap{
		PreviousFocus: key.NewBinding(
			key.WithKeys("["),
			key.WithHelp("[", "focus previous"),
		),
		NextFocus: key.NewBinding(
			key.WithKeys("]"),
			key.WithHelp("]", "focus next"),
		),
		PressButton: key.NewBinding(
			key.WithKeys("enter"),
			key.WithHelp("enter", "press button"),
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

type resetButtonKeyMap struct {
	PreviousFocus key.Binding
	NextFocus     key.Binding
	PressButton   key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k resetButtonKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextFocus, k.PressButton, k.Help, k.Quit}
}

func (k resetButtonKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{{k.NextFocus, k.PressButton, k.Help, k.Quit}}
}

func (rb *resetButton) KeyMap() help.KeyMap {
	return resetButtonKeyMap{
		PreviousFocus: key.NewBinding(
			key.WithKeys("["),
			key.WithHelp("[", "focus previous"),
		),
		NextFocus: key.NewBinding(
			key.WithKeys("]"),
			key.WithHelp("]", "focus next"),
		),
		PressButton: key.NewBinding(
			key.WithKeys("enter"),
			key.WithHelp("enter", "press button"),
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

// TODO: Need to combine the helps???

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

func (m *Model) KeyMap() help.KeyMap {
	if m.FormSection.Focused() {
		if m.appStatus == CreateSessionConfig {
			return m.FormSection.KeyMap()
		} else {
			return m.jsonview.KeyMap()
		}
	} else if m.HeaderSection.Focused() {
		return m.HeaderSection.KeyMap()
	} else if m.ResetButton.Focused() {
		return m.ResetButton.KeyMap()
	}

	panic("unreachable")
}
