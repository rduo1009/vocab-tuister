package listtui

import (
	"github.com/charmbracelet/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
)

func (m model) View() string {
	// Fill screen
	m.textarea.SetWidth(m.width)
	m.textarea.SetHeight(m.height - 6)

	// Components
	title := internal.TitleStyle.Render("Vocab List Creator")
	textArea := "\n" + m.textarea.View()
	keyControlInfo := internal.KeyControlsStyle.Render("\nctrl+c to quit • ctrl+s to save\n\n")

	// Combine
	text := lipgloss.JoinVertical(lipgloss.Left, title, textArea, keyControlInfo)
	return text
}
