package questioncomponents

import (
	"fmt"
	"strings"

	"charm.land/bubbles/v2/help"
	"charm.land/bubbles/v2/key"
	"charm.land/bubbles/v2/textinput"
	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type textinputWrapper struct {
	textinput.Model
	focused    bool
	pendingCmd tea.Cmd
}

func (ti *textinputWrapper) Focus() {
	ti.focused = true
	ti.pendingCmd = ti.Model.Focus()
}

func (ti *textinputWrapper) Blur() {
	ti.focused = false
	ti.Model.Blur()
}

func (ti *textinputWrapper) Focused() bool {
	return ti.focused
}

func (ti *textinputWrapper) TakePendingCmd() tea.Cmd {
	cmd := ti.pendingCmd
	ti.pendingCmd = nil
	return cmd
}

type TypeInQuestionModel struct {
	width, height int

	question  questions.Question
	textinput *textinputWrapper

	styles           *styles.StylesWrapper
	unansweredKeyMap unansweredTypeInKeyMap
	answeredKeyMap   answeredTypeInKeyMap
	status           QuestionStatus
}

func NewTypeInQuestionModel(question questions.Question, styles *styles.StylesWrapper) *TypeInQuestionModel {
	ti := textinput.New()
	ti.Blur()

	unansweredKeyMap := unansweredTypeInKeyMap{
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
	answeredKeyMap := answeredTypeInKeyMap{
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

	return &TypeInQuestionModel{
		question:         question,
		textinput:        &textinputWrapper{Model: ti},
		styles:           styles,
		unansweredKeyMap: unansweredKeyMap,
		answeredKeyMap:   answeredKeyMap,
		status:           Unanswered,
	}
}

func (m *TypeInQuestionModel) Focused() bool {
	return m.textinput.Focused()
}

type unansweredTypeInKeyMap struct {
	Submit        key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k unansweredTypeInKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.Submit, k.NextFocus, k.Help, k.Quit}
}

func (k unansweredTypeInKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.Submit, k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

type answeredTypeInKeyMap struct {
	NextQuestion  key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k answeredTypeInKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextQuestion, k.NextFocus, k.Help, k.Quit}
}

func (k answeredTypeInKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.NextQuestion, k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

func (m *TypeInQuestionModel) KeyMap() help.KeyMap {
	if m.status == Unanswered {
		return m.unansweredKeyMap
	}

	return m.answeredKeyMap
}

func (m *TypeInQuestionModel) Init() tea.Cmd {
	return tea.Sequence(
		textinput.Blink,
		util.MsgCmd(navigator.AddNavigableMsg{Components: []navigator.Navigable{m.textinput}}),
		util.MsgCmd(navigator.FocusNavigableMsg{Target: m.textinput}),
	)
}

func (m *TypeInQuestionModel) QuestionStatus() QuestionStatus {
	return m.status
}

func (m *TypeInQuestionModel) Update(msg tea.Msg) (QuestionModel, tea.Cmd) {
	var cmds []tea.Cmd

	if msg, ok := msg.(tea.KeyPressMsg); ok {
		switch {
		case key.Matches(msg, m.unansweredKeyMap.Submit):
			if m.status == Unanswered {
				correct := m.question.Check(strings.TrimSpace(m.textinput.Value()))
				if correct {
					m.status = Correct
				} else {
					m.status = Incorrect
				}

				cmds = append(cmds, util.MsgCmd(QuestionAnsweredMsg{}))

				break
			}

			fallthrough

		case key.Matches(msg, m.answeredKeyMap.NextQuestion):
			if m.status != Unanswered {
				return m, tea.Batch(
					util.MsgCmd(NextQuestionMsg{}),
					util.MsgCmd(
						navigator.RemoveNavigableMsg{
							Components: []navigator.Navigable{m.textinput},
						},
					),
				)
			}
		}
	}

	util.UpdaterVal(&cmds, &m.textinput.Model, msg)
	cmds = append(cmds, m.textinput.TakePendingCmd())

	return m, tea.Batch(cmds...)
}

func (m *TypeInQuestionModel) SetWidth(width int) {
	m.width = width
}

func (m *TypeInQuestionModel) SetHeight(height int) {
	m.height = height
}

func (m *TypeInQuestionModel) View() string {
	var promptView string
	switch q := m.question.(type) {
	case *questions.TypeInEngToLatQuestion:
		promptView = fmt.Sprintf(
			"%s %s %s",
			m.styles.Bold.Render("Translate"),
			m.styles.Text.Render("to Latin:"),
			m.styles.Italic.Render(q.Prompt),
		)

	case *questions.TypeInLatToEngQuestion:
		promptView = fmt.Sprintf(
			"%s %s %s",
			m.styles.Bold.Render("Translate"),
			m.styles.Text.Render("to English:"),
			m.styles.Italic.Render(q.Prompt),
		)

	case *questions.ParseWordCompToLatQuestion:
		promptView = fmt.Sprintf(
			"%s %s %s %s?",
			m.styles.Text.Render("What is"),
			m.styles.Italic.Render(q.Prompt),
			m.styles.Text.Render("in the"),
			q.Components,
		)

	default:
		panic("unreachable")
	}

	var inputView string
	switch m.status {
	case Unanswered:
		inputView = m.textinput.View()

	case Correct:
		m.textinput.Blur()
		s := m.textinput.Styles()
		s.Blurred.Text = m.styles.SessionPage.Correct // the only relevant style here
		m.textinput.SetStyles(s)
		inputView = m.textinput.View()

	case Incorrect:
		m.textinput.Blur()
		inputView = lipgloss.JoinHorizontal(
			lipgloss.Top,
			m.textinput.View(),
			m.styles.SessionPage.Incorrect.Render(" ✕ "+m.question.GetMainAnswer().(string)),
		)
	}

	return lipgloss.JoinVertical(lipgloss.Left, promptView, inputView)
}
