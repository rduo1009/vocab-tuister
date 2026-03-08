package session

import (
	"fmt"
	"strconv"
	"strings"

	"charm.land/bubbles/v2/key"
	tea "charm.land/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questioncomponents"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questions"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/dropdown"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/tabs"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

func (m *Model) Update(msg tea.Msg) (app.PageModel, tea.Cmd) {
	var cmds []tea.Cmd
	switch m.appStatus {
	case Unavailable:
		if *m.listLoaded == create.StatusLoaded && *m.configLoaded == create.StatusLoaded {
			m.appStatus = Uninitialised
			cmds = append(
				cmds,
				getQuestions(5500), // TODO: actual server port here
				util.MsgCmd(navigator.RemoveNavigableMsg{
					Components: []navigator.Navigable{m.returnButton},
				}),
			)
		} else {
			if msg, ok := msg.(tea.KeyPressMsg); ok &&
				key.Matches(msg, m.KeyMap().(unavailableKeyMap).PressButton) &&
				m.returnButton.Focused() {
				// set up returning back later
				m.appStatus = Unavailable
				m.currentIndex = 0
				m.answeredCount = 0
				m.correctCount = 0

				// return to create page
				return m, tea.Batch(
					util.MsgCmd(tabs.SelectTabMsg{Index: 0}),
					util.MsgCmd(navigator.RemoveNavigableMsg{Components: []navigator.Navigable{
						m.returnButton,
					}}),
				)
			}
		}

		fallthrough

	case Uninitialised:
		if msg, ok := msg.(QuestionsGetMsg); ok {
			m.questions = make([]questioncomponents.QuestionModel, len(msg.Questions))
			for i, q := range msg.Questions {
				switch q.QuestionMode() {
				case questions.Regular:
					m.questions[i] = questioncomponents.NewTypeInQuestionModel(q)

				case questions.ParseWord:
					m.questions[i] = questioncomponents.NewParseQuestionModel(q)

				case questions.PrincipalParts:
					m.questions[i] = questioncomponents.NewPrincipalPartsQuestionModel(q)

				case questions.MultipleChoice:
					m.questions[i] = questioncomponents.NewMultipleChoiceQuestionModel(q)
				}
			}

			m.appStatus = Initialised
			m.questionCount = len(m.questions)
			cmds = append(cmds, m.questions[m.currentIndex].Init())
		}

	case Initialised:
		switch msg := msg.(type) {
		case questioncomponents.QuestionAnsweredMsg:
			m.answeredCount++
			if m.questions[m.currentIndex].QuestionStatus() == questioncomponents.Correct {
				m.correctCount++
			}

		case questioncomponents.NextQuestionMsg:
			if m.currentIndex < m.questionCount-1 {
				m.currentIndex++
				return m, m.questions[m.currentIndex].Init()
			}

			m.appStatus = Completed

			return m, tea.Sequence(
				util.MsgCmd(navigator.AddNavigableMsg{
					Components: []navigator.Navigable{
						m.returnButton,
						m.restartButton,
					},
				}),
				util.MsgCmd(navigator.FocusNavigableMsg{Target: m.returnButton}),
			)

		case dropdown.StartMsg:
			if strings.HasPrefix(msg.ID, "parsequestionDropdown") {
				finalChar := string(msg.ID[len(msg.ID)-1])

				index, err := strconv.Atoi(finalChar)
				if err != nil {
					cmds = append(
						cmds,
						util.MsgCmd(app.ErrMsg(fmt.Errorf(
							"failed to convert %s to integer: %w",
							finalChar,
							err,
						))),
					)
				}

				m.dropdownActive = true
				m.activeDropdownIndex = index
			}

		case dropdown.PickedMsg:
			if strings.HasPrefix(msg.ID, "parsequestionDropdown") {
				m.dropdownActive = false
			}

		case dropdown.ExitMsg:
			if strings.HasPrefix(msg.ID, "parsequestionDropdown") {
				m.dropdownActive = false
			}
		}

		if q, ok := m.questions[m.currentIndex].(*questioncomponents.ParseQuestionModel); ok &&
			m.dropdownActive {
			util.UpdaterVal(&cmds, &q.Dropdowns[m.activeDropdownIndex].Dropdown, msg)
		} else {
			util.UpdaterVal(&cmds, &m.questions[m.currentIndex], msg)
		}

	case Completed:
		if msg, ok := msg.(tea.KeyPressMsg); ok && key.Matches(msg, m.KeyMap().(completedKeyMap).PressButton) {
			switch {
			case m.returnButton.Focused():
				// set up returning back later
				m.appStatus = Unavailable
				m.currentIndex = 0
				m.answeredCount = 0
				m.correctCount = 0

				// return to create page
				return m, tea.Batch(
					util.MsgCmd(tabs.SelectTabMsg{Index: 0}),
					util.MsgCmd(navigator.RemoveNavigableMsg{
						Components: []navigator.Navigable{
							m.returnButton,
							m.restartButton,
						},
					}),
				)

			case m.restartButton.Focused():
				m.appStatus = Unavailable
				m.currentIndex = 0
				m.answeredCount = 0
				m.correctCount = 0
				cmds = append(cmds, m.Init())
			}
		}
	}

	return m, tea.Batch(cmds...)
}
