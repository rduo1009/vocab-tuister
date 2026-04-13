package session

import (
	"charm.land/bubbles/v2/help"
	"charm.land/bubbles/v2/key"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questioncomponents"
)

type unavailableKeyMap struct {
	PressButton   key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k unavailableKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.PressButton, k.NextFocus, k.Help, k.Quit}
}

func (k unavailableKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.PressButton, k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

type loadingKeyMap struct {
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k loadingKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextFocus, k.Help, k.Quit}
}

func (k loadingKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

type completedKeyMap struct {
	PressButton   key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k completedKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.PressButton, k.NextFocus, k.Help, k.Quit}
}

func (k completedKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.PressButton, k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

func (m *Model) KeyMap() help.KeyMap {
	if m.dropdownActive {
		return m.questions[m.currentIndex].(*questioncomponents.ParseQuestionModel).
			Dropdowns[m.activeDropdownIndex].KeyMap()
	}

	switch m.appStatus {
	case Unavailable:
		return unavailableKeyMap{
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

	case Uninitialised:
		return loadingKeyMap{
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

	case Initialised:
		return m.questions[m.currentIndex].KeyMap()

	case Completed:
		return completedKeyMap{
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

	default:
		panic("unreachable")
	}
}
