package config

import (
	"charm.land/bubbles/v2/help"
	"charm.land/bubbles/v2/key"
)

type headerSectionKeyMap struct {
	PressButton   key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k headerSectionKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextFocus, k.PressButton, k.Help, k.Quit}
}

func (k headerSectionKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.PressButton, k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

func (hs *headerSection) KeyMap() headerSectionKeyMap {
	return headerSectionKeyMap{
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

type resetButtonKeyMap struct {
	PressButton   key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k resetButtonKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextFocus, k.PressButton, k.Help, k.Quit}
}

func (k resetButtonKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.PressButton, k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

func (rb *resetButton) KeyMap() resetButtonKeyMap {
	return resetButtonKeyMap{
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

type formSectionKeyMap struct {
	fs            *formSection
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k formSectionKeyMap) ShortHelp() []key.Binding {
	return append(
		[]key.Binding{k.NextFocus},
		append(k.fs.form.KeyBinds(), k.Help, k.Quit)...,
	)
}

func (k formSectionKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.PreviousFocus, k.NextFocus},
		k.fs.form.KeyBinds(),
		{k.Help, k.Quit},
	}
}

func (fs *formSection) KeyMap() help.KeyMap {
	return formSectionKeyMap{
		fs: fs,
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
	switch {
	case m.FormSection.Focused():
		if m.AppStatus == CreateSessionConfig {
			return m.FormSection.KeyMap()
		}

		return m.jsonview.KeyMap()

	case m.HeaderSection.Focused():
		return m.HeaderSection.KeyMap()

	case m.ResetButton.Focused():
		return m.ResetButton.KeyMap()

	default:
		panic("unreachable")
	}
}
