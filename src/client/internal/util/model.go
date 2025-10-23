package util

import (
	"github.com/charmbracelet/bubbles/v2/help"
	tea "github.com/charmbracelet/bubbletea/v2"
)

// ComponentModel is a variant of tea.Model which uses string views instead of tea.View.
//
// NOTE: The support in bubbletea v2 for the new tea.View seems to be incomplete or smth
// bc no support for e.g. combining two tea.View, also the bubbles have not been updated either
// The charm devs themselves use:
// https://github.com/charmbracelet/crush/blob/d04566f04b2151dc15c83fd78f414ae0d5793332/internal/tui/util/util.go#L14
type ComponentModel interface {
	Init() tea.Cmd
	Update(tea.Msg) (ComponentModel, tea.Cmd)
	View() string

	SetWidth(int)
	SetHeight(int)

	KeyMap() help.KeyMap
}
