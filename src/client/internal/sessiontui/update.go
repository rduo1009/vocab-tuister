package sessiontui

import (
	"github.com/charmbracelet/bubbles/v2/key"
	tea "github.com/charmbracelet/bubbletea/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
	"github.com/rduo1009/vocab-tuister/src/client/pkg"
	"github.com/rduo1009/vocab-tuister/src/client/pkg/enums"
	"github.com/rduo1009/vocab-tuister/src/client/pkg/questions"
)

type (
	errMsg    struct{ err error }
	initOkMsg struct {
		vocabList     string
		sessionConfig pkg.SessionConfig
		questions     questions.Questions
	}
)

func (m *model) changeSelectionPrincipalPartsTextnputs(requiredPPTextinputs int) []tea.Cmd {
	ppcmds := make([]tea.Cmd, requiredPPTextinputs)
	for i := range requiredPPTextinputs {
		if i == m.selectedOption-1 {
			ppcmds[i] = m.principalPartsTextinputs[i].Focus()
			m.principalPartsTextinputs[i].PromptStyle = internal.TextinputFocusedStyle
			m.principalPartsTextinputs[i].TextStyle = internal.TextinputFocusedStyle
			continue
		}

		m.principalPartsTextinputs[i].Blur()
		m.principalPartsTextinputs[i].PromptStyle = internal.NoStyle
		m.principalPartsTextinputs[i].TextStyle = internal.NoStyle
	}
	return ppcmds
}

func (m *model) updatePrincipalPartsTextnputs(msg tea.Msg) tea.Cmd {
	cmds := make([]tea.Cmd, len(m.principalPartsTextinputs))

	for i := range m.principalPartsTextinputs {
		m.principalPartsTextinputs[i], cmds[i] = m.principalPartsTextinputs[i].Update(msg)
	}

	return tea.Batch(cmds...)
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd
	var cmd tea.Cmd

	// Check if Init has ran yet
	switch msg := msg.(type) {
	case initOkMsg:
		m.vocabList = msg.vocabList
		m.sessionConfig = msg.sessionConfig
		m.questions = msg.questions
		m.initialised = true

	case errMsg:
		m.err = msg.err
		return m, tea.Quit
	}

	// If not, wait for it to run
	if !m.initialised {
		return m, nil
	}

	// If Init has ran, continue as normal
	numberOptions := m.sessionConfig.NumberMultiplechoiceOptions
	m.questionMode = questions.QuestionMode(m.questions[m.currentQuestion-1])
	currentQuestionStruct := m.questions[m.currentQuestion-1]

	var requiredPPTextinputs int
	if m.questionMode == enums.PrincipalParts {
		requiredPPTextinputs = len(currentQuestionStruct.(*questions.PrincipalPartsQuestion).PrincipalParts)
	}

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		switch {
		case key.Matches(msg, m.keys.Up):
			if m.appStatus == enums.Unanswered {
				switch m.questionMode {
				case enums.MultipleChoice:
					if m.selectedOption != 1 {
						m.selectedOption--
					}

				case enums.PrincipalParts:
					if m.selectedOption != 1 {
						m.selectedOption--
					}

					cmds = append(cmds, m.changeSelectionPrincipalPartsTextnputs(requiredPPTextinputs)...)
				}
			}

		case key.Matches(msg, m.keys.Down):
			if m.appStatus == enums.Unanswered {
				switch m.questionMode {
				case enums.MultipleChoice:
					if m.selectedOption != numberOptions {
						m.selectedOption++
					}

				case enums.PrincipalParts:
					if m.selectedOption != requiredPPTextinputs {
						m.selectedOption++
					}

					cmds = append(cmds, m.changeSelectionPrincipalPartsTextnputs(requiredPPTextinputs)...)
				}
			}

		case key.Matches(msg, m.keys.NextOption):
			if m.appStatus == enums.Unanswered {
				switch m.questionMode {
				case enums.MultipleChoice:
					if m.selectedOption == numberOptions {
						m.selectedOption = 1
					} else {
						m.selectedOption++
					}

				case enums.PrincipalParts:
					if m.selectedOption == requiredPPTextinputs {
						m.selectedOption = 1
					} else {
						m.selectedOption++
					}

					cmds = append(cmds, m.changeSelectionPrincipalPartsTextnputs(requiredPPTextinputs)...)
				}
			}

		case key.Matches(msg, m.keys.Submit):
			if m.appStatus == enums.Unanswered {
				var correct bool

				switch m.questionMode {
				case enums.Regular:
					correct = questions.Check(currentQuestionStruct, m.textinput.Value())

				case enums.PrincipalParts:
					var response []string
					for i := range requiredPPTextinputs {
						response = append(response, m.principalPartsTextinputs[i].Value())
					}
					correct = questions.Check(currentQuestionStruct, response)

				case enums.MultipleChoice:
					selectedOptionString := questions.GetChoices(currentQuestionStruct)[m.selectedOption-1]
					correct = questions.Check(currentQuestionStruct, selectedOptionString)
				}

				if correct {
					m.appStatus = enums.Correct
					m.score++
				} else {
					m.appStatus = enums.Incorrect
				}
			} else {
				if m.currentQuestion == len(m.questions) {
					return m, tea.Quit
				}

				// Reset variables
				m.currentQuestion++
				m.appStatus = enums.Unanswered
				m.selectedOption = 1

				m.questionMode = questions.QuestionMode(m.questions[m.currentQuestion-1])
				currentQuestionStruct := m.questions[m.currentQuestion-1]

				if m.questionMode == enums.PrincipalParts {
					requiredPPTextinputs = len(currentQuestionStruct.(*questions.PrincipalPartsQuestion).PrincipalParts)
				}

				// Reset textinputs
				m.textinput.Reset()

				for i := range requiredPPTextinputs {
					m.principalPartsTextinputs[i].Reset()

					if i == 0 {
						m.principalPartsTextinputs[i].Focus()
						m.principalPartsTextinputs[i].PromptStyle = internal.TextinputFocusedStyle
						m.principalPartsTextinputs[i].TextStyle = internal.TextinputFocusedStyle
						continue
					}

					m.principalPartsTextinputs[i].Blur()
					m.principalPartsTextinputs[i].PromptStyle = internal.NoStyle
					m.principalPartsTextinputs[i].TextStyle = internal.NoStyle
				}
			}

		case key.Matches(msg, m.keys.Help):
			m.help.ShowAll = !m.help.ShowAll

		case key.Matches(msg, m.keys.Quit):
			return m, tea.Quit
		}

	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height

	case errMsg:
		m.err = msg.err
		return m, tea.Quit
	}

	if m.appStatus == enums.Unanswered {
		switch m.questionMode {
		case enums.Regular:
			m.textinput, cmd = m.textinput.Update(msg)

		case enums.PrincipalParts:
			cmd = m.updatePrincipalPartsTextnputs(msg)
		}
	}
	cmds = append(cmds, cmd)

	return m, tea.Batch(cmds...)
}
