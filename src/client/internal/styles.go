package internal

import (
	"os"

	"github.com/charmbracelet/lipgloss"
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
	NoStyle     = lipgloss.NewStyle()
	FaintStyle  = lipgloss.NewStyle().Faint(true)
	ItalicStyle = lipgloss.NewStyle().Italic(true)
	BoldStyle   = lipgloss.NewStyle().Bold(true)

	TitleStyle       = lipgloss.NewStyle().Bold(true).Underline(true).Width(physicalWidth).Align(lipgloss.Center)
	LesserTitleStyle = BoldStyle.Underline(true)

	SelectedStyle = lipgloss.NewStyle().
			Foreground(lipgloss.AdaptiveColor{Light: darkOrange, Dark: lightOrange})
	CheckedStyle         = BoldStyle
	SelectedCheckedStyle = lipgloss.NewStyle().Inherit(SelectedStyle).Inherit(CheckedStyle)

	TextinputFocusedStyle = lipgloss.NewStyle().Foreground(lipgloss.AdaptiveColor{Light: darkPink, Dark: lightPink})
	ChoiceSelectedStyle   = lipgloss.NewStyle().Foreground(lipgloss.AdaptiveColor{Light: darkPink, Dark: lightPink})
	CorrectStyle          = BoldStyle.Foreground(lipgloss.AdaptiveColor{Light: darkGreen, Dark: lightGreen})
	IncorrectStyle        = BoldStyle.Foreground(lipgloss.AdaptiveColor{Light: darkRed, Dark: lightRed})
)
