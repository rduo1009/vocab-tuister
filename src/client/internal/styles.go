package internal

import (
	"os"

	"github.com/charmbracelet/lipgloss/v2"
	lipglosscompat "github.com/charmbracelet/lipgloss/v2/compat"
	"golang.org/x/term"
)

var physicalWidth, _, _ = term.GetSize(int(os.Stdout.Fd()))

// Colours used by the tui.
// Some colours are taken from https://github.com/elewis787/boa/blob/develop/styles.go.
const (
	lightTeal   = `#03dac5`
	darkTeal    = `#01a299`
	lightOrange = `#e17b35`
	darkOrange  = `#da5a03`
	lightPink   = `#ff3399`
	darkPink    = `#c06`
	lightRed    = `#ff4d4d`
	darkRed     = `#ff1a1a`
	lightGreen  = `#4dff4d`
	darkGreen   = `#1aff1a`
)

var (
	NoStyle          = lipgloss.NewStyle()
	TitleStyle       = lipgloss.NewStyle().Width(physicalWidth).Align(lipgloss.Center).Bold(true)
	LesserTitleStyle = lipgloss.NewStyle().Bold(true).Underline(true)
	FaintStyle       = lipgloss.NewStyle().Faint(true)
	ItalicStyle      = lipgloss.NewStyle().Italic(true)

	SelectedStyle        = lipgloss.NewStyle().Foreground(lipglosscompat.AdaptiveColor{Light: darkOrange, Dark: lightOrange})
	CheckedStyle         = lipgloss.NewStyle().Bold(true)
	SelectedCheckedStyle = lipgloss.NewStyle().Inherit(SelectedStyle).Inherit(CheckedStyle)

	TextinputFocusedStyle = lipgloss.NewStyle().Foreground(lipglosscompat.AdaptiveColor{Light: darkPink, Dark: lightPink})
	ChoiceSelectedStyle   = lipgloss.NewStyle().Foreground(lipglosscompat.AdaptiveColor{Light: darkPink, Dark: lightPink})
	CorrectStyle          = lipgloss.NewStyle().Bold(true).Foreground(lipglosscompat.AdaptiveColor{Light: darkGreen, Dark: lightGreen})
	IncorrectStyle        = lipgloss.NewStyle().Bold(true).Foreground(lipglosscompat.AdaptiveColor{Light: darkRed, Dark: lightRed})
)
