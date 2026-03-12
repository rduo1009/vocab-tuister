package questioncomponents

import (
	"fmt"
	"math/rand"
	"slices"
	"strings"

	"charm.land/bubbles/v2/help"
	"charm.land/bubbles/v2/key"
	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions/endingcomponents"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/dropdown"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type dropdownWrapper struct {
	Dropdown *dropdown.Model
	focused  bool
}

func (d *dropdownWrapper) Focus() {
	d.focused = true
}

func (d *dropdownWrapper) Blur() {
	d.focused = false
}

func (d *dropdownWrapper) Focused() bool {
	return d.focused
}

type ParseQuestionModel struct {
	width, height int

	question            questions.Question
	Dropdowns           []*dropdownWrapper
	numberDropdowns     int
	activeDropdownIndex int

	unansweredKeyMap unansweredParseKeyMap
	answeredKeyMap   answeredParseKeyMap
	pos              endingcomponents.PartOfSpeech
	components       endingcomponents.EndingComponents
	status           QuestionStatus
}

func NewParseQuestionModel(question questions.Question) *ParseQuestionModel {
	answerEndingComponents := question.(*questions.ParseWordLatToCompQuestion).Answers

	var possiblePOS []endingcomponents.PartOfSpeech
	for _, component := range answerEndingComponents {
		if x := component.PartOfSpeech(); !slices.Contains(possiblePOS, x) {
			possiblePOS = append(possiblePOS, x)
		}
	}

	// Some verb forms can have different amounts of components, just pick one
	var chosenPOS endingcomponents.PartOfSpeech
	if len(possiblePOS) > 1 {
		chosenPOS = possiblePOS[rand.Intn(len(possiblePOS))]
	} else {
		chosenPOS = possiblePOS[0]
	}

	var (
		numberDropdowns int
		dropdowns       []*dropdownWrapper
	)

	switch chosenPOS {
	case endingcomponents.Noun:
		numberDropdowns = 2
		dropdowns = []*dropdownWrapper{
			{Dropdown: dropdown.New("parsequestionDropdown0", endingcomponents.Cases)},
			{Dropdown: dropdown.New("parsequestionDropdown1", endingcomponents.Numbers)},
		}

	case endingcomponents.Pronoun:
		numberDropdowns = 3
		dropdowns = []*dropdownWrapper{
			{Dropdown: dropdown.New("parsequestionDropdown0", endingcomponents.Cases)},
			{Dropdown: dropdown.New("parsequestionDropdown1", endingcomponents.Numbers)},
			{Dropdown: dropdown.New("parsequestionDropdown2", endingcomponents.Genders)},
		}

	case endingcomponents.Adjective:
		numberDropdowns = 4
		dropdowns = []*dropdownWrapper{
			{Dropdown: dropdown.New("parsequestionDropdown0", endingcomponents.Cases)},
			{Dropdown: dropdown.New("parsequestionDropdown1", endingcomponents.Numbers)},
			{Dropdown: dropdown.New("parsequestionDropdown2", endingcomponents.Genders)},
			{Dropdown: dropdown.New("parsequestionDropdown3", endingcomponents.Degrees)},
		}

	case endingcomponents.Verb:
		numberDropdowns = 5
		dropdowns = []*dropdownWrapper{
			{Dropdown: dropdown.New("parsequestionDropdown0", endingcomponents.Tenses)},
			{Dropdown: dropdown.New("parsequestionDropdown1", endingcomponents.Voices)},
			{Dropdown: dropdown.New("parsequestionDropdown2", endingcomponents.Moods)},
			{Dropdown: dropdown.New("parsequestionDropdown3", endingcomponents.Persons)},
			{Dropdown: dropdown.New("parsequestionDropdown4", endingcomponents.Numbers)},
		}

	case endingcomponents.VerbalNoun:
		numberDropdowns = 2
		dropdowns = []*dropdownWrapper{
			{Dropdown: dropdown.New("parsequestionDropdown0", endingcomponents.Moods)},
			{Dropdown: dropdown.New("parsequestionDropdown1", endingcomponents.Cases)},
		}

	case endingcomponents.ParticiplePOS:
		numberDropdowns = 6
		dropdowns = []*dropdownWrapper{
			{Dropdown: dropdown.New("parsequestionDropdown0", endingcomponents.Tenses)},
			{Dropdown: dropdown.New("parsequestionDropdown1", endingcomponents.Voices)},
			{Dropdown: dropdown.New("parsequestionDropdown2", endingcomponents.Moods)},
			{Dropdown: dropdown.New("parsequestionDropdown3", endingcomponents.Cases)},
			{Dropdown: dropdown.New("parsequestionDropdown4", endingcomponents.Numbers)},
			{Dropdown: dropdown.New("parsequestionDropdown5", endingcomponents.Genders)},
		}

	case endingcomponents.InfinitivePOS:
		numberDropdowns = 3
		dropdowns = []*dropdownWrapper{
			{Dropdown: dropdown.New("parsequestionDropdown0", endingcomponents.Tenses)},
			{Dropdown: dropdown.New("parsequestionDropdown1", endingcomponents.Voices)},
			{Dropdown: dropdown.New("parsequestionDropdown2", endingcomponents.Moods)},
		}

	case endingcomponents.Adverb:
		numberDropdowns = 1
		dropdowns = []*dropdownWrapper{
			{Dropdown: dropdown.New("parsequestionDropdown0", endingcomponents.Degrees)},
		}

	case endingcomponents.RegularWord:
		panic("unreachable")
	}

	var endingComponents endingcomponents.EndingComponents
	for _, d := range dropdowns {
		if setter, ok := d.Dropdown.LastSelected.(endingcomponents.ComponentSetter); ok {
			setter.SetComponent(&endingComponents)
		}
	}

	unansweredKeyMap := unansweredParseKeyMap{
		OpenDropdown: key.NewBinding(
			key.WithKeys("enter"),
			key.WithHelp("enter", "open dropdown"),
		),
		Submit: key.NewBinding(
			key.WithKeys("ctrl+enter"),
			key.WithHelp("ctrl+enter", "submit"),
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
	answeredKeyMap := answeredParseKeyMap{
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

	return &ParseQuestionModel{
		question:         question,
		Dropdowns:        dropdowns,
		numberDropdowns:  numberDropdowns,
		unansweredKeyMap: unansweredKeyMap,
		answeredKeyMap:   answeredKeyMap,
		pos:              chosenPOS,
		components:       endingComponents,
		status:           Unanswered,
	}
}

type unansweredParseKeyMap struct {
	OpenDropdown  key.Binding
	Submit        key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k unansweredParseKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.OpenDropdown, k.Submit, k.NextFocus, k.Help, k.Quit}
}

func (k unansweredParseKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.OpenDropdown, k.Submit, k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

type answeredParseKeyMap struct {
	NextQuestion  key.Binding
	PreviousFocus key.Binding
	NextFocus     key.Binding
	Help          key.Binding
	Quit          key.Binding
}

func (k answeredParseKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.NextQuestion, k.NextFocus, k.Help, k.Quit}
}

func (k answeredParseKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.NextQuestion, k.PreviousFocus, k.NextFocus},
		{k.Help, k.Quit},
	}
}

func (m *ParseQuestionModel) KeyMap() help.KeyMap {
	if m.status == Unanswered {
		return m.unansweredKeyMap
	}

	return m.answeredKeyMap
}

func (m *ParseQuestionModel) Init() tea.Cmd {
	navigables := make([]navigator.Navigable, m.numberDropdowns)
	for i := range m.Dropdowns {
		navigables[i] = m.Dropdowns[i]
	}

	return tea.Sequence(
		util.MsgCmd(navigator.AddNavigableMsg{Components: navigables}),
		util.MsgCmd(navigator.FocusNavigableMsg{Target: navigables[0]}),
	)
}

func (m *ParseQuestionModel) QuestionStatus() QuestionStatus {
	return m.status
}

// Update updates the question model.
// Note that this does not update the dropdowns themselves. This should be handled by the main page model instead.
func (m *ParseQuestionModel) Update(msg tea.Msg) (QuestionModel, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		switch {
		case key.Matches(msg, m.unansweredKeyMap.OpenDropdown):
			if m.status == Unanswered {
				for i, d := range m.Dropdowns {
					if d.Focused() {
						m.activeDropdownIndex = i
						cmds = append(
							cmds,
							util.MsgCmd(dropdown.StartMsg{
								ID: fmt.Sprintf("parsequestionDropdown%d", i),
							}),
						)

						break
					}
				}

				break
			}

			fallthrough

		case key.Matches(msg, m.unansweredKeyMap.Submit):
			if m.status == Unanswered {
				correct := m.question.Check(m.components)
				if correct {
					m.status = Correct
				} else {
					m.status = Incorrect
				}

				cmds = append(cmds, tea.Batch(
					util.MsgCmd(QuestionAnsweredMsg{}),
				))

				break
			}

			fallthrough

		case key.Matches(msg, m.answeredKeyMap.NextQuestion):
			if m.status != Unanswered {
				navigables := make([]navigator.Navigable, m.numberDropdowns)
				for i := range m.Dropdowns {
					navigables[i] = m.Dropdowns[i]
				}

				return m, tea.Batch(
					util.MsgCmd(NextQuestionMsg{}),
					util.MsgCmd(navigator.RemoveNavigableMsg{Components: navigables}),
				)
			}
		}

	case dropdown.PickedMsg:
		if strings.HasPrefix(msg.ID, "parsequestionDropdown") {
			if setter, ok := msg.ChosenItem.(endingcomponents.ComponentSetter); ok {
				setter.SetComponent(&m.components)
			}
		}
	}

	return m, tea.Batch(cmds...)
}

func (m *ParseQuestionModel) SetWidth(width int) {
	m.width = width
}

func (m *ParseQuestionModel) SetHeight(height int) {
	m.height = height
}

func buttonStyle(focused bool) lipgloss.Style {
	if focused {
		return lipgloss.NewStyle().
			Foreground(lipgloss.Color("#fff7db")).
			Background(lipgloss.Color("#888b7e")).
			Italic(true).
			Underline(true).
			MarginLeft(1).
			Padding(0, 1)
	}

	return lipgloss.NewStyle().
		Foreground(lipgloss.Color("#fff7db")).
		Background(lipgloss.Color("#888b7e")).
		MarginLeft(1).
		Padding(0, 1)
}

func (m *ParseQuestionModel) View() string {
	promptView := fmt.Sprintf(
		"%s this Latin word: %s",
		internal.BoldStyle.Render("Parse"),
		internal.ItalicStyle.Render(m.question.GetPrompt()),
	)

	dropdownViews := make([]string, m.numberDropdowns)
	for i, d := range m.Dropdowns {
		dropdownViews[i] = buttonStyle(d.Focused()).
			Width(d.Dropdown.GetWidth()).
			Render(d.Dropdown.LastSelected.String())
	}

	var resultView string
	switch m.status {
	case Correct:
		resultView = correctStyle.Render(" ✓")

	case Incorrect:
		resultView = incorrectStyle.Render(
			" ✕ " + m.question.(*questions.ParseWordLatToCompQuestion).MainAnswer.String(),
		)
	}

	inputView := lipgloss.JoinHorizontal(lipgloss.Top, dropdownViews...)

	return lipgloss.JoinVertical(
		lipgloss.Left,
		promptView,
		lipgloss.JoinHorizontal(lipgloss.Top, inputView, resultView),
	)
}
