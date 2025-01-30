package sessiontui

import (
	"fmt"
	"strings"

	"github.com/charmbracelet/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
	"github.com/rduo1009/vocab-tuister/src/client/pkg/enums"
	"github.com/rduo1009/vocab-tuister/src/client/pkg/questions"
)

func questionStringRegular(q questions.Question) string {
	switch q := q.(type) {
	case *questions.TypeInEngtoLatQuestion:
		return fmt.Sprintf("%s to Latin: %s", internal.BoldStyle.Render("Translate"), internal.ItalicStyle.Render(q.Prompt))
	case *questions.TypeInLattoEngQuestion:
		return fmt.Sprintf("%s to English: %s", internal.BoldStyle.Render("Translate"), internal.ItalicStyle.Render(q.Prompt))
	case *questions.ParseWordLattoCompQuestion:
		return fmt.Sprintf("%s this Latin word: %s", internal.BoldStyle.Render("Parse"), internal.ItalicStyle.Render(q.Prompt))
	case *questions.ParseWordComptoLatQuestion:
		return fmt.Sprintf("What is %s in the %s?", internal.ItalicStyle.Render(q.Prompt), q.Components)
	}
	panic(fmt.Sprintf("Question type could not be recognised. (got %T)", q))
}

func questionStringPrincipalParts(q questions.Question) string {
	return fmt.Sprintf("Principal parts of %s", internal.ItalicStyle.Render(q.(*questions.PrincipalPartsQuestion).Prompt))
}

func questionStringMultipleChoice(q questions.Question) string {
	switch q := q.(type) {
	case *questions.MultipleChoiceEngtoLatQuestion:
		return fmt.Sprintf("%s to Latin: %s", internal.BoldStyle.Render("Translate"), internal.ItalicStyle.Render(q.Prompt))
	case *questions.MultipleChoiceLatToEngQuestion:
		return fmt.Sprintf("%s to English: %s", internal.BoldStyle.Render("Translate"), internal.ItalicStyle.Render(q.Prompt))
	}
	panic(fmt.Sprintf("Question type could not be recognised. (got %T)", q))
}

func (m model) View() string {
	if m.err != nil {
		return fmt.Sprint(m.err) + "\n"
	}

	if !m.initialised {
		return ""
	}

	currentQuestionStruct := m.questions[m.currentQuestion-1]

	var b strings.Builder

	b.WriteString(internal.TitleStyle.Render("Vocab Tester Session"))
	b.WriteRune('\n')
	b.WriteString(fmt.Sprintf("Question %d/%d", m.currentQuestion, len(m.questions)))
	b.WriteString("\n\n")

	switch m.questionMode {
	case enums.Regular:
		m.textinput.SetWidth(m.width)

		b.WriteString(questionStringRegular(currentQuestionStruct))
		b.WriteRune('\n')
		switch m.appStatus {
		case enums.Unanswered:
			m.textinput.TextStyle = internal.NoStyle
			b.WriteString(m.textinput.View())

		case enums.Correct:
			m.textinput.Blur()
			m.textinput.TextStyle = internal.CorrectStyle
			b.WriteString(m.textinput.View())

		case enums.Incorrect:
			m.textinput.Blur()
			b.WriteString(lipgloss.JoinHorizontal(
				lipgloss.Top,
				m.textinput.View(),
				internal.IncorrectStyle.Render(fmt.Sprintf(" ✕ %s", questions.GetMainAnswer(currentQuestionStruct).(string))),
			))
		}

	case enums.PrincipalParts:
		requiredPPTextinputs := len(currentQuestionStruct.(*questions.PrincipalPartsQuestion).PrincipalParts)

		m.textinput.SetWidth(m.width)

		b.WriteString(questionStringPrincipalParts(currentQuestionStruct))
		b.WriteRune('\n')

		switch m.appStatus {
		case enums.Unanswered:
			for i := range requiredPPTextinputs {
				b.WriteString(m.principalPartsTextinputs[i].View())

				if i < requiredPPTextinputs-1 {
					b.WriteRune('\n')
				}
			}

		case enums.Correct:
			for i := range requiredPPTextinputs {
				m.textinput.Blur()
				m.principalPartsTextinputs[i].TextStyle = internal.CorrectStyle
				b.WriteString(m.principalPartsTextinputs[i].View())

				if i < requiredPPTextinputs-1 {
					b.WriteRune('\n')
				}
			}

		case enums.Incorrect:
			for i := range requiredPPTextinputs {
				m.textinput.Blur()
				if x := questions.GetMainAnswer(currentQuestionStruct).([]string)[i]; m.principalPartsTextinputs[i].Value() != x {
					b.WriteString(lipgloss.JoinHorizontal(
						lipgloss.Top,
						m.principalPartsTextinputs[i].View(),
						internal.IncorrectStyle.Render(fmt.Sprintf(" ✕ %s", x)),
					))
				} else {
					b.WriteString(m.principalPartsTextinputs[i].View())
				}

				if i < requiredPPTextinputs-1 {
					b.WriteRune('\n')
				}
			}
		}

	case enums.MultipleChoice:
		b.WriteString(questionStringMultipleChoice(currentQuestionStruct))
		b.WriteRune('\n')
		for i, choice := range questions.GetChoices(currentQuestionStruct) {
			if m.selectedOption == i+1 {
				switch m.appStatus {
				case enums.Unanswered:
					b.WriteString(choiceString(choice, "selected"))
				case enums.Correct:
					b.WriteString(choiceString(choice, "correct"))
				case enums.Incorrect:
					b.WriteString(choiceString(choice, "incorrect"))
				}
			} else {
				b.WriteString(choiceString(choice, "unselected"))
			}
			b.WriteRune('\n')
		}
	}

	b.WriteString("\n")

	switch m.appStatus {
	case enums.Unanswered:
		b.WriteString("\n\n")
		if m.currentQuestion == 1 {
			b.WriteString("Score: 0/0 (0%)\n")
		} else {
			b.WriteString(fmt.Sprintf("Score: %d/%d (%.0f%%)\n", m.score, m.currentQuestion-1, 100*float64(m.score)/float64(m.currentQuestion-1)))
		}
	case enums.Correct:
		b.WriteString("Answer is correct!\n\n")
		b.WriteString(fmt.Sprintf("Score: %d/%d (%.0f%%)\n", m.score, m.currentQuestion, 100*float64(m.score)/float64(m.currentQuestion)))
	case enums.Incorrect:
		b.WriteString("Answer is incorrect!\n\n")
		b.WriteString(fmt.Sprintf("Score: %d/%d (%.0f%%)\n", m.score, m.currentQuestion, 100*float64(m.score)/float64(m.currentQuestion)))
	}

	b.WriteString(m.help.View(m.keys))

	return b.String()
}

func choiceString(choice, status string) string {
	if status == "correct" {
		return internal.CorrectStyle.Render("[x] " + choice)
	}

	if status == "incorrect" {
		return internal.IncorrectStyle.Render("[x] " + choice)
	}

	if status == "selected" {
		return fmt.Sprint(internal.ChoiceSelectedStyle.Render("[ ] " + choice))
	}

	return fmt.Sprint("[ ] " + choice)
}
