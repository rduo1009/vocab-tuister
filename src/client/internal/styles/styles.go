package styles

import (
	"charm.land/lipgloss/v2"
	tint "github.com/lrstanley/bubbletint/v2"
)

type StylesWrapper struct{ Styles }

func inactiveTabBorder() lipgloss.Border {
	b := lipgloss.NormalBorder()
	b.Top = "─"
	b.Bottom = "─"
	b.Left = "│"
	b.Right = "│"
	b.TopLeft = "╭"
	b.TopRight = "╮"
	b.BottomLeft = "┴"
	b.BottomRight = "┴"

	return b
}

func activeTabBorder() lipgloss.Border {
	b := lipgloss.NormalBorder()
	b.Top = "─"
	b.Bottom = " "
	b.Left = "│"
	b.Right = "│"
	b.TopLeft = "╭"
	b.TopRight = "╮"
	b.BottomLeft = "┘"
	b.BottomRight = "└"
	return b
}

type Styles struct {
	// General

	Title  lipgloss.Style
	Bold   lipgloss.Style
	Italic lipgloss.Style

	// Borders

	TabBorder          func(pad int) lipgloss.Style
	TabBorderActive    lipgloss.Style
	TabBorderInactive  lipgloss.Style
	TabBorderFocused   lipgloss.Style
	TabBorderUnfocused lipgloss.Style

	NormalBorderFocused   lipgloss.Style
	NormalBorderUnfocused lipgloss.Style

	// Small components

	Button          lipgloss.Style
	ButtonActive    lipgloss.Style
	ButtonInactive  lipgloss.Style
	ButtonFocused   lipgloss.Style
	ButtonUnfocused lipgloss.Style

	// Create page load section

	LabelMissing lipgloss.Style
	LabelPending lipgloss.Style
	LabelLoaded  lipgloss.Style
	LabelSep     lipgloss.Style

	// Session page

	Correct   lipgloss.Style
	Incorrect lipgloss.Style
}

func DefaultStyles(theme *tint.Tint) Styles {
	return Styles{
		Title:  lipgloss.NewStyle().Bold(true).Underline(true),
		Bold:   lipgloss.NewStyle().Bold(true),
		Italic: lipgloss.NewStyle().Italic(true),

		TabBorder: func(pad int) lipgloss.Style {
			return lipgloss.NewStyle().Padding(0, pad)
		},
		TabBorderActive:    lipgloss.NewStyle().Border(activeTabBorder(), true),
		TabBorderInactive:  lipgloss.NewStyle().Border(inactiveTabBorder(), true),
		TabBorderFocused:   lipgloss.NewStyle().BorderForeground(theme.Blue),
		TabBorderUnfocused: lipgloss.NewStyle().BorderForeground(theme.White),

		NormalBorderFocused:   lipgloss.NewStyle().BorderForeground(theme.Blue),
		NormalBorderUnfocused: lipgloss.NewStyle().BorderForeground(theme.White),

		Button: lipgloss.NewStyle().Padding(0, 1),
		ButtonActive: lipgloss.NewStyle().
			Foreground(lipgloss.Color("#fff7db")).
			Background(lipgloss.Color("#888b7e")),
		ButtonInactive: lipgloss.NewStyle().
			Foreground(lipgloss.Color("#a9a9a9")).
			Background(lipgloss.Color("#555555")),
		ButtonFocused:   lipgloss.NewStyle().Italic(true).Underline(true),
		ButtonUnfocused: lipgloss.NewStyle(),

		LabelMissing: lipgloss.NewStyle().Foreground(theme.Red),
		LabelPending: lipgloss.NewStyle().Foreground(theme.Yellow),
		LabelLoaded:  lipgloss.NewStyle().Foreground(theme.Green),
		LabelSep:     lipgloss.NewStyle().Foreground(lipgloss.Lighten(theme.Black, 0.1)),

		Correct:   lipgloss.NewStyle().Bold(true).Foreground(theme.Green),
		Incorrect: lipgloss.NewStyle().Bold(true).Foreground(theme.Red),
	}
}
