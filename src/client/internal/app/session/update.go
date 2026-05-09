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
		if *m.listVerified == create.StatusVerified && *m.configVerified == create.StatusVerified {
			m.appStatus = Uninitialised
			cmds = append(
				cmds,
				getQuestions(m.serverPort, *m.vocabList, *m.sessionConfig, *m.numberOfQuestions),
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
		if msg, ok := msg.(QuestionStreamGetMsg); ok {
			m.questionProvider = msg.QuestionProvider

			q, err := m.questionProvider.Next()
			if err != nil {
				cmds = append(cmds, util.MsgCmd(app.ErrMsg(err)))
				break
			}

			switch q.QuestionMode() {
			case questions.Regular:
				m.currentQuestionModel = questioncomponents.NewTypeInQuestionModel(q, m.styles)

			case questions.ParseWord:
				m.currentQuestionModel = questioncomponents.NewParseQuestionModel(q, m.styles)

			case questions.PrincipalParts:
				m.currentQuestionModel = questioncomponents.NewPrincipalPartsQuestionModel(q, m.styles)

			case questions.MultipleChoice:
				m.currentQuestionModel = questioncomponents.NewMultipleChoiceQuestionModel(q, m.styles)
			}

			m.appStatus = Initialised
			cmds = append(cmds, m.currentQuestionModel.Init())
		}

	case Initialised:
		switch msg := msg.(type) {
		case questioncomponents.QuestionAnsweredMsg:
			m.answeredCount++
			if m.currentQuestionModel.QuestionStatus() == questioncomponents.Correct {
				m.correctCount++
			}

		case questioncomponents.NextQuestionMsg:
			if m.questionProvider.Current() >= *m.numberOfQuestions {
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
			}

			q, err := m.questionProvider.Next()
			if err != nil {
				cmds = append(cmds, util.MsgCmd(app.ErrMsg(err)))
			}

			switch q.QuestionMode() {
			case questions.Regular:
				m.currentQuestionModel = questioncomponents.NewTypeInQuestionModel(q, m.styles)

			case questions.ParseWord:
				m.currentQuestionModel = questioncomponents.NewParseQuestionModel(q, m.styles)

			case questions.PrincipalParts:
				m.currentQuestionModel = questioncomponents.NewPrincipalPartsQuestionModel(q, m.styles)

			case questions.MultipleChoice:
				m.currentQuestionModel = questioncomponents.NewMultipleChoiceQuestionModel(q, m.styles)
			}

			return m, m.currentQuestionModel.Init()

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

		if q, ok := m.currentQuestionModel.(*questioncomponents.ParseQuestionModel); ok &&
			m.dropdownActive {
			util.UpdaterVal(&cmds, &q.Dropdowns[m.activeDropdownIndex].Model, msg)
		} else {
			util.UpdaterVal(&cmds, &m.currentQuestionModel, msg)
		}

	case Completed:
		if msg, ok := msg.(tea.KeyPressMsg); ok && key.Matches(msg, m.KeyMap().(completedKeyMap).PressButton) {
			switch {
			case m.returnButton.Focused():
				// set up returning back later
				m.appStatus = Unavailable
				m.answeredCount = 0
				m.correctCount = 0
				m.questionProvider.Close()

				// return to create page; no need to remove navigables as this will be done anyway
				return m, util.MsgCmd(tabs.SelectTabMsg{Index: 0})

			case m.restartButton.Focused():
				m.appStatus = Unavailable
				m.answeredCount = 0
				m.correctCount = 0
				m.questionProvider.Close()

				cmds = append(cmds, m.Init())
			}
		}
	}

	return m, tea.Batch(cmds...)
}
