package configtui

import (
	"fmt"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
)

func (m model) View() string {
	text := ""

	if m.mcOptionsNumberPage {
		m.textinput.SetWidth(m.width)

		text += "Input the number of options wanted for multiple-choice questions.\n"
		text += m.textinput.View() + "\n"
		text += internal.FaintStyle.Render("(press right to save and quit)")
		return text
	}

	currentPage := m.wizard.Pages[m.currentPage]

	text += internal.LesserTitleStyle.Render(currentPage.Title) + "\n"
	for i, setting := range currentPage.Settings {
		settingSelected := i == m.selectedOption
		text += checkbox(setting.DisplayName, setting.Checked, settingSelected) + "\n"
	}

	text += m.help.View(m.keys)
	return text
}

func checkbox(setting string, checked, selected bool) string {
	if selected && checked {
		return internal.SelectedCheckedStyle.Render("[x] " + setting)
	}

	if checked {
		return internal.CheckedStyle.Render("[x] " + setting)
	}

	if selected {
		return fmt.Sprint(internal.SelectedStyle.Render("[ ] " + setting))
	}

	return fmt.Sprint("[ ] " + setting)
}
