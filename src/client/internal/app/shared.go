package app

import (
	"charm.land/bubbles/v2/help"
	tea "charm.land/bubbletea/v2"
)

type ErrMsg error

// ComponentModel is a variant of tea.Model which uses string views instead of `tea.View`.
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
