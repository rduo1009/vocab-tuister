package listtui

import (
	"fmt"
	"strings"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
)

func (m Model) View() string {
	if m.err != nil {
		return fmt.Sprint(m.err) + "\n"
	}

	var b strings.Builder

	m.textarea.SetWidth(m.width)
	if m.help.ShowAll {
		m.textarea.SetHeight(m.height - 6)
	} else {
		m.textarea.SetHeight(m.height - 3)
	}

	b.WriteString(internal.TitleStyle.Render("Vocab List Creator\n"))
	b.WriteString("\n" + m.textarea.View() + "\n")
	b.WriteString(m.help.View(m.keys))

	return b.String()
}
