package list

import (
	"github.com/charmbracelet/bubbles/v2/help"
	"github.com/charmbracelet/bubbles/v2/key"
)

type headerSectionKeyMap struct {
	OpenDropdown  key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k headerSectionKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextFocus, k.OpenDropdown, k.Help, k.Quit}
}

func (k headerSectionKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.OpenDropdown, k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

func (hs *headerSection) KeyMap() headerSectionKeyMap {
	return headerSectionKeyMap{
		PreviousFocus: key.NewBinding(
			key.WithKeys("["),
			key.WithHelp("[", "focus previous"),
		),
		NextFocus: key.NewBinding(
			key.WithKeys("]"),
			key.WithHelp("]", "focus next"),
		),
		OpenDropdown: key.NewBinding(
			key.WithKeys("enter"),
			key.WithHelp("enter", "open dropdown"),
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

type vocabEditorKeyMap struct {
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k vocabEditorKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextFocus, k.Help, k.Quit}
}

func (k vocabEditorKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

func VocabEditorKeyMap() vocabEditorKeyMap {
	return vocabEditorKeyMap{
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

type selectButtonKeyMap struct {
	PreviousFocus key.Binding
	NextFocus     key.Binding
	PressButton   key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k selectButtonKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextFocus, k.PressButton, k.Help, k.Quit}
}

func (k selectButtonKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{{k.PressButton, k.PreviousFocus, k.NextFocus}, {k.Help, k.Quit}}
}

func (sb *selectButton) KeyMap() selectButtonKeyMap {
	return selectButtonKeyMap{
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

func (m *Model) KeyMap() help.KeyMap {
	if m.HeaderSection.Focused() {
		return m.HeaderSection.KeyMap()
	} else if m.VocabEditor.Focused() {
		return VocabEditorKeyMap()
	} else if m.SelectButton.Focused() {
		return m.SelectButton.KeyMap()
	}

	panic("unreachable")
}
