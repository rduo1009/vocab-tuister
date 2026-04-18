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
	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
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

	styles           *styles.StylesWrapper
	unansweredKeyMap unansweredMultipleChoiceKeyMap
	answeredKeyMap   answeredMultipleChoiceKeyMap
	status           QuestionStatus
}

func NewMultipleChoiceQuestionModel(
	question questions.Question,
	styles *styles.StylesWrapper,
) *MultipleChoiceQuestionModel {
	choices := question.(questions.MultipleChoiceQuestion).GetChoices()

	options := make([]*optionWrapper, len(choices))
	for i, option := range choices {
		options[i] = &optionWrapper{
			Value:   option,
			focused: i == 0,
		}
	}

	unansweredKeyMap := unansweredMultipleChoiceKeyMap{
		ChooseOption: key.NewBinding(
			key.WithKeys(""),
			key.WithHelp("1 2 3 ...", "choose option"),
		),
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
		styles:           styles,
		unansweredKeyMap: unansweredKeyMap,
		answeredKeyMap:   answeredKeyMap,
		status:           Unanswered,
	}
}

func (m *MultipleChoiceQuestionModel) Focused() bool {
	for i := range m.numberOptions {
		if m.options[i].Focused() {
			m.currentOptionIndex = i
			return true
		}
	}
	return false
}

type unansweredMultipleChoiceKeyMap struct {
	ChooseOption  key.Binding
	Submit        key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k unansweredMultipleChoiceKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.ChooseOption, k.Submit, k.NextFocus, k.Help, k.Quit}
}

func (k unansweredMultipleChoiceKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.ChooseOption, k.Submit, k.PreviousFocus, k.NextFocus},
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

func (m *MultipleChoiceQuestionModel) checkResponse() {
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
}

func (m *MultipleChoiceQuestionModel) Update(msg tea.Msg) (QuestionModel, tea.Cmd) {
	var cmds []tea.Cmd

	if msg, ok := msg.(tea.KeyPressMsg); ok {
		if m.status == Unanswered {
			// Check for digit keys first.
			//
			// msg.Code is a rune (int32) representing the pressed key. In Unicode,
			// the digit characters '0'-'9' are laid out contiguously at code points
			// 48-57. So this check is equivalent to: msg.Code >= 48 && msg.Code <= 57.
			// Letters like 'a' (97) or 'A' (65) fall outside this range entirely,
			// so they won't match.
			if msg.Code >= '0' && msg.Code <= '9' {
				// Convert the rune to the integer digit it represents.
				//
				// Because '0'-'9' are contiguous, subtracting '0' (48) gives the
				// digit's value: '0'-'0'=0, '1'-'0'=1, ..., '9'-'0'=9.
				// The outer int() converts from rune (int32) to int, since we want
				// to use this as an index.
				digit := int(msg.Code - '0')
				if digit > 0 && digit <= m.numberOptions {
					m.currentOptionIndex = digit - 1 // e.g. "1" selects option 0
				}

				m.checkResponse()
				return m, tea.Batch(
					util.MsgCmd(navigator.FocusNavigableMsg{
						Target: m.options[m.currentOptionIndex],
					}),
					util.MsgCmd(QuestionAnsweredMsg{}),
				)
			} else if key.Matches(msg, m.unansweredKeyMap.Submit) {
				for i := range m.numberOptions {
					if m.options[i].Focused() {
						m.currentOptionIndex = i
						break
					}
				}

				m.checkResponse()
				return m, util.MsgCmd(QuestionAnsweredMsg{})
			}
		} else if key.Matches(msg, m.answeredKeyMap.NextQuestion) {
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

	return m, tea.Batch(cmds...)
}

func (m *MultipleChoiceQuestionModel) SetWidth(width int) {
	m.width = width
}

func (m *MultipleChoiceQuestionModel) SetHeight(height int) {
	m.height = height
}

func (m *MultipleChoiceQuestionModel) View() string {
	var promptView string
	switch q := m.question.(type) {
	case *questions.MultipleChoiceEngToLatQuestion:
		promptView = fmt.Sprintf(
			"%s to Latin: %s",
			m.styles.Bold.Render("Translate"),
			m.styles.Italic.Render(q.Prompt),
		)

	case *questions.MultipleChoiceLatToEngQuestion:
		promptView = fmt.Sprintf(
			"%s to English: %s",
			m.styles.Bold.Render("Translate"),
			m.styles.Italic.Render(q.Prompt),
		)

	default:
		panic("unreachable")
	}

	// TODO: refactor def poss here
	var optionColor color.Color
	optionViews := make([]string, m.numberOptions)
	switch m.status {
	case Unanswered:
		for i := range m.numberOptions {
			optionViews[i] = m.styles.MultipleChoice.Option(m.options[i].Focused(), m.styles.MultipleChoice.Unanswered).
				Width(m.width).
				Render(m.options[i].Value)
		}

	case Correct:
		for i := range m.numberOptions {
			if i == m.correctSelectedOptionIndex {
				optionColor = m.styles.MultipleChoice.Correct
			} else {
				optionColor = m.styles.MultipleChoice.Unanswered
			}

			optionViews[i] = m.styles.MultipleChoice.Option(m.options[i].Focused(), optionColor).
				Width(m.width).
				Render(m.options[i].Value)
		}

	case Incorrect:
		for i := range m.numberOptions {
			switch i {
			case m.correctSelectedOptionIndex:
				optionColor = m.styles.MultipleChoice.Correct

			case m.incorrectSelectedOptionIndex:
				optionColor = m.styles.MultipleChoice.Incorrect

			default:
				optionColor = m.styles.MultipleChoice.Unanswered
			}

			optionViews[i] = m.styles.MultipleChoice.Option(m.options[i].Focused(), optionColor).
				Width(m.width).
				Render(m.options[i].Value)
		}

	default:
		panic("unreachable")
	}

	inputView := lipgloss.JoinVertical(lipgloss.Left, optionViews...)

	return lipgloss.JoinVertical(lipgloss.Left, promptView, inputView)
}
