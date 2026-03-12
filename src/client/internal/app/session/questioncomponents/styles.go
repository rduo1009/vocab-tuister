package questioncomponents

import (
	"charm.land/lipgloss/v2"
	lipglosscompat "charm.land/lipgloss/v2/compat"
)

// TODO: REMOVE THIS WHEN CREATING GLOBAL STYLES.

const (
	lightRed   = `#ff4d4d`
	darkRed    = `#ff1a1a`
	lightGreen = `#4dff4d`
	darkGreen  = `#1aff1a`
)

var (
	boldStyle   = lipgloss.NewStyle().Bold(true)
	italicStyle = lipgloss.NewStyle().Italic(true)

	correctStyle = boldStyle.Foreground(
		lipglosscompat.AdaptiveColor{Light: lipgloss.Color(darkGreen), Dark: lipgloss.Color(lightGreen)},
	)
	incorrectStyle = boldStyle.Foreground(
		lipglosscompat.AdaptiveColor{Light: lipgloss.Color(darkRed), Dark: lipgloss.Color(lightRed)},
	)
)
