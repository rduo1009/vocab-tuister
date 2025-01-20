package configtui

import (
	"fmt"
	"strings"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
)

func (m model) View() string {
	if m.err != nil {
		return fmt.Sprint(m.err) + "\n"
	}

	var b strings.Builder

	if m.mcOptionsNumberPage {
		m.textinput.SetWidth(m.width)

		b.WriteString("Input the number of options wanted for multiple-choice questions.\n")
		b.WriteString(m.textinput.View() + "\n")
		b.WriteString(internal.FaintStyle.Render("(press right to save and quit)"))
		return b.String()
	}

	currentPage := m.wizard.Pages[m.currentPage]

	b.WriteString(internal.LesserTitleStyle.Render(currentPage.Title) + "\n")
	for i, setting := range currentPage.Settings {
		settingSelected := i == m.selectedOption
		b.WriteString(checkboxString(setting.DisplayName, setting.Checked, settingSelected) + "\n")
	}

	b.WriteString(m.help.View(m.keys))
	return b.String()
}

func checkboxString(setting string, checked, selected bool) string {
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
