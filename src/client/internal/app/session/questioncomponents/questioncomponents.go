package questioncomponents

import (
	"charm.land/bubbles/v2/help"
	tea "charm.land/bubbletea/v2"
)

type (
	NextQuestionMsg     struct{}
	QuestionAnsweredMsg struct{}
)

type QuestionStatus int

const (
	Unanswered QuestionStatus = iota
	Correct
	Incorrect
)

// XXX: Can the need for QuestionStatus be removed entirely eventually?
type QuestionModel interface {
	Init() tea.Cmd
	Update(msg tea.Msg) (QuestionModel, tea.Cmd)
	View() string

	SetWidth(width int)
	SetHeight(height int)

	KeyMap() help.KeyMap

	QuestionStatus() QuestionStatus
}
