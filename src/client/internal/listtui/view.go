package listtui

import (
	"github.com/charmbracelet/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
)

func (m model) View() string {
	// Fill screen
	m.textarea.SetWidth(m.width)
	if m.help.ShowAll {
		m.textarea.SetHeight(m.height - 6)
	} else {
		m.textarea.SetHeight(m.height - 3)
	}

	// Components
	title := internal.TitleStyle.Render("Vocab List Creator")
	textArea := "\n" + m.textarea.View()
	helpInfo := m.help.View(m.keys)

	// Combine
	text := lipgloss.JoinVertical(lipgloss.Left, title, textArea, helpInfo)
	return text
}
