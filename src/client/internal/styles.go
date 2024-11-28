package internal

import (
	"os"

	"github.com/charmbracelet/lipgloss/v2"
	"golang.org/x/term"
)

var physicalWidth, _, _ = term.GetSize(int(os.Stdout.Fd()))

var (
	KeyControlsStyle = lipgloss.NewStyle().Bold(true)
	TitleStyle       = lipgloss.NewStyle().Width(physicalWidth).Align(lipgloss.Center).Bold(true)
)
