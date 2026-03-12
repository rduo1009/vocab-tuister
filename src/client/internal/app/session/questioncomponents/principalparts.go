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
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type PrincipalPartsQuestionModel struct {
	width, height int

	question         questions.Question
	textinputs       []*textinputWrapper
	numberTextinputs int

	unansweredKeyMap unansweredPrincipalPartsKeyMap
	answeredKeyMap   answeredPrincipalPartsKeyMap
	status           QuestionStatus
}

func NewPrincipalPartsQuestionModel(question questions.Question) *PrincipalPartsQuestionModel {
	pp := question.(*questions.PrincipalPartsQuestion).PrincipalParts

	tis := make([]*textinputWrapper, len(pp))
	for i := range pp {
		ti := textinput.New()
		tis[i] = &textinputWrapper{Textinput: ti}
	}

	unansweredKeyMap := unansweredPrincipalPartsKeyMap{
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
	answeredKeyMap := answeredPrincipalPartsKeyMap{
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

	return &PrincipalPartsQuestionModel{
		question:         question,
		textinputs:       tis,
		numberTextinputs: len(pp),
		unansweredKeyMap: unansweredKeyMap,
		answeredKeyMap:   answeredKeyMap,
		status:           Unanswered,
	}
}

type unansweredPrincipalPartsKeyMap struct {
	Submit        key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k unansweredPrincipalPartsKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.Submit, k.NextFocus, k.Help, k.Quit}
}

func (k unansweredPrincipalPartsKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.Submit, k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

type answeredPrincipalPartsKeyMap struct {
	NextQuestion  key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k answeredPrincipalPartsKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextQuestion, k.NextFocus, k.Help, k.Quit}
}

func (k answeredPrincipalPartsKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.NextQuestion, k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

func (m *PrincipalPartsQuestionModel) KeyMap() help.KeyMap {
	if m.status == Unanswered {
		return m.unansweredKeyMap
	}

	return m.answeredKeyMap
}

func (m *PrincipalPartsQuestionModel) Init() tea.Cmd {
	navigables := make([]navigator.Navigable, m.numberTextinputs)
	for i := range m.textinputs {
		navigables[i] = m.textinputs[i]
	}

	return tea.Sequence(
		textinput.Blink,
		util.MsgCmd(navigator.AddNavigableMsg{Components: navigables}),
		util.MsgCmd(navigator.FocusNavigableMsg{Target: navigables[0]}),
	)
}

func (m *PrincipalPartsQuestionModel) QuestionStatus() QuestionStatus {
	return m.status
}

func (m *PrincipalPartsQuestionModel) Update(msg tea.Msg) (QuestionModel, tea.Cmd) {
	var cmds []tea.Cmd

	if msg, ok := msg.(tea.KeyPressMsg); ok {
		switch {
		case key.Matches(msg, m.unansweredKeyMap.Submit):
			if m.status == Unanswered {
				response := make([]string, m.numberTextinputs)
				for i := range m.textinputs {
					response[i] = m.textinputs[i].Textinput.Value()
				}

				correct := m.question.Check(response)
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
				navigables := make([]navigator.Navigable, m.numberTextinputs)
				for i := range m.textinputs {
					navigables[i] = m.textinputs[i]
				}

				return m, tea.Batch(
					util.MsgCmd(NextQuestionMsg{}),
					util.MsgCmd(navigator.RemoveNavigableMsg{Components: navigables}),
				)
			}
		}
	}

	for _, ti := range m.textinputs {
		if m.status != Unanswered {
			if _, ok := msg.(tea.KeyPressMsg); !ok {
				util.UpdaterVal(&cmds, &ti.Textinput, msg)
			}
		} else {
			util.UpdaterVal(&cmds, &ti.Textinput, msg)
			cmds = append(cmds, ti.TakePendingCmd())
		}
	}

	return m, tea.Batch(cmds...)
}

func (m *PrincipalPartsQuestionModel) SetWidth(width int) {
	m.width = width
}

func (m *PrincipalPartsQuestionModel) SetHeight(height int) {
	m.height = height
}

func (m *PrincipalPartsQuestionModel) View() string {
	promptView := fmt.Sprintf(
		"%s of %s",
		boldStyle.Render("Principal parts"),
		italicStyle.Render(m.question.GetPrompt()),
	)

	tiViews := make([]string, m.numberTextinputs)
	for i, ti := range m.textinputs {
		switch m.status {
		case Correct:
			s := ti.Textinput.Styles()
			s.Focused.Text = correctStyle
			s.Blurred.Text = correctStyle
			ti.Textinput.SetStyles(s)

		case Incorrect:
			if x := m.question.GetMainAnswer().([]string)[i]; m.textinputs[i].Textinput.Value() != x {
				s := ti.Textinput.Styles()
				s.Focused.Text = incorrectStyle
				s.Blurred.Text = incorrectStyle
				ti.Textinput.SetStyles(s)
			}
		}

		tiViews[i] = ti.Textinput.View()
	}

	inputView := lipgloss.JoinVertical(lipgloss.Left, tiViews...)

	var footerView string
	if m.status == Incorrect {
		footerView = incorrectStyle.Render(
			"✕ " + strings.Join(m.question.(*questions.PrincipalPartsQuestion).PrincipalParts, ", "),
		)
	}

	return lipgloss.JoinVertical(lipgloss.Left, promptView, inputView, footerView)
}
