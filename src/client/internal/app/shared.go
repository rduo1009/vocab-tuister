package app

import (
	"charm.land/bubbles/v2/help"
	tea "charm.land/bubbletea/v2"
)

type ErrMsg error

// TODO: See if https://github.com/charmbracelet/crush/blob/e9b59c4b8cd7c6613cd48e533dd6b319c6bd7c69/internal/ui/common/interface.go#L8
// is better (using generic), then refactor?

// ComponentModel is a variant of tea.Model which uses string views instead of tea.View.
//
// NOTE: The support in bubbletea v2 for the new tea.View seems to be incomplete or smth
// bc no support for e.g. combining two tea.View, also the bubbles have not been updated either
// The charm devs themselves use:
// https://github.com/charmbracelet/crush/blob/d04566f04b2151dc15c83fd78f414ae0d5793332/internal/tui/util/util.go#L14
type ComponentModel interface {
	Init() tea.Cmd
	Update(msg tea.Msg) (ComponentModel, tea.Cmd)
	View() string

	SetWidth(width int)
	SetHeight(height int)

	KeyMap() help.KeyMap
}

// PageModel is a variant of ComponentModel which adds overlay-related functions.
type PageModel interface {
	Init() tea.Cmd
	Update(msg tea.Msg) (PageModel, tea.Cmd)
	View() string

	SetWidth(width int)
	SetHeight(height int)

	KeyMap() help.KeyMap

	HasOverlay() bool
	OverlayView(width, height int) (view string, x, y int)
}
