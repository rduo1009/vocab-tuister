package questioncomponents

import (
	"fmt"
	"image/color"

	"charm.land/bubbles/v2/help"
	"charm.land/bubbles/v2/key"
	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type optionWrapper struct {
	Value   string
	focused bool
}

func (o *optionWrapper) Focus() {
	o.focused = true
}

func (o *optionWrapper) Blur() {
	o.focused = false
}

func (o *optionWrapper) Focused() bool {
	return o.focused
}

type MultipleChoiceQuestionModel struct {
	width, height int

	question           questions.Question
	options            []*optionWrapper
	numberOptions      int
	currentOptionIndex int

	// Aids with displaying feedback after user submits
	incorrectSelectedOptionIndex int
	correctSelectedOptionIndex   int

	unansweredKeyMap unansweredMultipleChoiceKeyMap
	answeredKeyMap   answeredMultipleChoiceKeyMap
	status           QuestionStatus
}

func NewMultipleChoiceQuestionModel(question questions.Question) *MultipleChoiceQuestionModel {
	choices := question.(questions.MultipleChoiceQuestion).GetChoices()

	options := make([]*optionWrapper, len(choices))
	for i, option := range choices {
		options[i] = &optionWrapper{
			Value:   option,
			focused: i == 0,
		}
	}

	unansweredKeyMap := unansweredMultipleChoiceKeyMap{
		Submit: key.NewBinding(
			key.WithKeys("enter", "ctrl+enter"),
			key.WithHelp("enter", "submit"),
		),
		PreviousFocus: key.NewBinding(
			key.WithKeys("["),
			key.WithHelp("[", "focus previous"),
		),
		NextFocus: key.NewBinding(
			key.WithKeys("]"),
			key.WithHelp("]", "focus next"),
		),
		Help: key.NewBinding(
			key.WithKeys("ctrl+h"),
			key.WithHelp("ctrl+h", "toggle additional help"),
		),
		Quit: key.NewBinding(
			key.WithKeys("ctrl+q", "ctrl+c"),
			key.WithHelp("ctrl+q", "quit"),
		),
	}
	answeredKeyMap := answeredMultipleChoiceKeyMap{
		NextQuestion: key.NewBinding(
			key.WithKeys("enter", "ctrl+enter"),
			key.WithHelp("enter", "next question"),
		),
		PreviousFocus: key.NewBinding(
			key.WithKeys("["),
			key.WithHelp("[", "focus previous"),
		),
		NextFocus: key.NewBinding(
			key.WithKeys("]"),
			key.WithHelp("]", "focus next"),
		),
		Help: key.NewBinding(
			key.WithKeys("ctrl+h"),
			key.WithHelp("ctrl+h", "toggle additional help"),
		),
		Quit: key.NewBinding(
			key.WithKeys("ctrl+q", "ctrl+c"),
			key.WithHelp("ctrl+q", "quit"),
		),
	}

	return &MultipleChoiceQuestionModel{
		question:         question,
		options:          options,
		numberOptions:    len(options),
		unansweredKeyMap: unansweredKeyMap,
		answeredKeyMap:   answeredKeyMap,
		status:           Unanswered,
	}
}

// TODO: add press 1, 2, 3, ... for multichoice.
type unansweredMultipleChoiceKeyMap struct {
	Submit        key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k unansweredMultipleChoiceKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.Submit, k.NextFocus, k.Help, k.Quit}
}

func (k unansweredMultipleChoiceKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.Submit, k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

type answeredMultipleChoiceKeyMap struct {
	NextQuestion  key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k answeredMultipleChoiceKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextQuestion, k.NextFocus, k.Help, k.Quit}
}

func (k answeredMultipleChoiceKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.NextQuestion, k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

func (m *MultipleChoiceQuestionModel) KeyMap() help.KeyMap {
	if m.status == Unanswered {
		return m.unansweredKeyMap
	}

	return m.answeredKeyMap
}

func (m *MultipleChoiceQuestionModel) Init() tea.Cmd {
	navigables := make([]navigator.Navigable, m.numberOptions)
	for i := range m.options {
		navigables[i] = m.options[i]
	}

	return tea.Sequence(
		util.MsgCmd(navigator.AddNavigableMsg{Components: navigables}),
		util.MsgCmd(navigator.FocusNavigableMsg{Target: navigables[0]}),
	)
}

func (m *MultipleChoiceQuestionModel) QuestionStatus() QuestionStatus {
	return m.status
}

func (m *MultipleChoiceQuestionModel) Update(msg tea.Msg) (QuestionModel, tea.Cmd) {
	var cmds []tea.Cmd

	if msg, ok := msg.(tea.KeyPressMsg); ok {
		switch {
		case key.Matches(msg, m.unansweredKeyMap.Submit):
			if m.status == Unanswered {
				for i := range m.numberOptions {
					if m.options[i].Focused() {
						m.currentOptionIndex = i
						break
					}
				}

				response := m.options[m.currentOptionIndex].Value

				correct := m.question.Check(response)
				if correct {
					m.status = Correct
					m.correctSelectedOptionIndex = m.currentOptionIndex
				} else {
					m.status = Incorrect

					m.incorrectSelectedOptionIndex = m.currentOptionIndex
					for i := range m.options { // look for the actual correct option
						if m.question.Check(m.options[i].Value) {
							m.correctSelectedOptionIndex = i
							break
						}
					}
				}

				cmds = append(cmds, util.MsgCmd(QuestionAnsweredMsg{}))

				break
			}

			fallthrough

		case key.Matches(msg, m.answeredKeyMap.NextQuestion):
			if m.status != Unanswered {
				navigables := make([]navigator.Navigable, m.numberOptions)
				for i := range m.options {
					navigables[i] = m.options[i]
				}

				return m, tea.Batch(
					util.MsgCmd(NextQuestionMsg{}),
					util.MsgCmd(
						navigator.RemoveNavigableMsg{
							Components: navigables,
						},
					),
				)
			}
		}
	}

	return m, tea.Batch(cmds...)
}

func (m *MultipleChoiceQuestionModel) SetWidth(width int) {
	m.width = width
}

func (m *MultipleChoiceQuestionModel) SetHeight(height int) {
	m.height = height
}

func optionStyle(focused bool, status QuestionStatus) lipgloss.Style {
	var borderColor color.Color

	switch status {
	case Unanswered:
		if focused {
			borderColor = lipgloss.Color("#FFFFFF")
		} else {
			borderColor = lipgloss.Color("#DCDCDC")
		}

	case Correct:
		if focused {
			borderColor = lipgloss.Color("#22C55E")
		} else {
			borderColor = lipgloss.Color("#BBF7D0")
		}

	case Incorrect:
		if focused {
			borderColor = lipgloss.Color("#F05252")
		} else {
			borderColor = lipgloss.Color("#FCA5A5")
		}
	}

	return lipgloss.NewStyle().
		Padding(0, 4).
		MarginBottom(1).
		Border(lipgloss.NormalBorder()).
		BorderForeground(borderColor).
		Align(lipgloss.Left)
}

func (m *MultipleChoiceQuestionModel) View() string {
	var promptView string
	switch q := m.question.(type) {
	case *questions.MultipleChoiceEngToLatQuestion:
		promptView = fmt.Sprintf(
			"%s to Latin: %s",
			boldStyle.Render("Translate"),
			italicStyle.Render(q.Prompt),
		)

	case *questions.MultipleChoiceLatToEngQuestion:
		promptView = fmt.Sprintf(
			"%s to English: %s",
			boldStyle.Render("Translate"),
			italicStyle.Render(q.Prompt),
		)

	default:
		panic("unreachable")
	}

	// TODO: refactor def poss here
	var optionStatus QuestionStatus

	optionViews := make([]string, m.numberOptions)
	switch m.status {
	case Unanswered:
		for i := range m.numberOptions {
			optionViews[i] = optionStyle(m.options[i].Focused(), Unanswered).
				Width(m.width).
				Render(m.options[i].Value)
		}

	case Correct:
		for i := range m.numberOptions {
			if i == m.correctSelectedOptionIndex {
				optionStatus = Correct
			} else {
				optionStatus = Unanswered
			}

			optionViews[i] = optionStyle(m.options[i].Focused(), optionStatus).
				Width(m.width).
				Render(m.options[i].Value)
		}

	case Incorrect:
		for i := range m.numberOptions {
			switch i {
			case m.correctSelectedOptionIndex:
				optionStatus = Correct

			case m.incorrectSelectedOptionIndex:
				optionStatus = Incorrect

			default:
				optionStatus = Unanswered
			}

			optionViews[i] = optionStyle(m.options[i].Focused(), optionStatus).
				Width(m.width).
				Render(m.options[i].Value)
		}
	}

	inputView := lipgloss.JoinVertical(lipgloss.Left, optionViews...)

	return lipgloss.JoinVertical(lipgloss.Left, promptView, inputView)
}
