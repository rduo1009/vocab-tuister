package internal

import (
	"os"

	"github.com/charmbracelet/lipgloss/v2"
	"golang.org/x/term"
)

var physicalWidth, _, _ = term.GetSize(int(os.Stdout.Fd()))

var (
	TitleStyle           = lipgloss.NewStyle().Width(physicalWidth).Align(lipgloss.Center).Bold(true)
	LesserTitleStyle     = lipgloss.NewStyle().Bold(true).Underline(true)
	FaintStyle           = lipgloss.NewStyle().Faint(true)
	KeyControlsStyle     = lipgloss.NewStyle().Bold(true)
	SelectedStyle        = lipgloss.NewStyle().Foreground(lipgloss.Color("#7E2FCC"))
	CheckedStyle         = lipgloss.NewStyle().Bold(true)
	SelectedCheckedStyle = lipgloss.NewStyle().Inherit(SelectedStyle).Inherit(CheckedStyle)
)
