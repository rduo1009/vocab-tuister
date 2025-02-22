package sessiontui

import (
	"github.com/charmbracelet/bubbles/v2/help"
	"github.com/charmbracelet/bubbles/v2/textinput"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
	"github.com/rduo1009/vocab-tuister/src/client/pkg"
	"github.com/rduo1009/vocab-tuister/src/client/pkg/enums"
	"github.com/rduo1009/vocab-tuister/src/client/pkg/questions"
)

type Model struct {
	textinput                textinput.Model
	principalPartsTextinputs []textinput.Model
	help                     help.Model
	keys                     KeyMap
	sessionConfigPath        string
	sessionConfig            pkg.SessionConfig
	vocabListPath            string
	vocabList                string
	numberOfQuestions        int
	serverPort               int
	questions                questions.Questions
	currentQuestion          int
	selectedOption           int
	questionMode             enums.QuestionMode
	appStatus                enums.AppStatus
	score                    int
	width                    int
	height                   int
	initialised              bool
	err                      error
}

const maximumPrincipalParts = 4

func InitialModel(sessionConfigPath, vocabListPath string, numberOfQuestions, serverPort int) Model {
	ti := textinput.New()
	ti.Placeholder = "Write answer here..."
	ti.Focus()

	principalPartsTextinputs := make([]textinput.Model, maximumPrincipalParts)
	var ppti textinput.Model
	for i := range principalPartsTextinputs {
		ppti = textinput.New()
		switch i {
		case 0:
			ppti.Placeholder = "First principal part"
			ppti.Focus()
			ppti.PromptStyle = internal.TextinputFocusedStyle
			ppti.TextStyle = internal.TextinputFocusedStyle
		case 1:
			ppti.Placeholder = "Second principal part"
		case 2:
			ppti.Placeholder = "Third principal part"
		case 3:
			ppti.Placeholder = "Fourth principal part"
		}
		principalPartsTextinputs[i] = ppti
	}

	m := Model{
		textinput:                ti,
		principalPartsTextinputs: principalPartsTextinputs,
		help:                     help.New(),
		keys:                     DefaultKeyMap,
		sessionConfigPath:        sessionConfigPath,
		vocabListPath:            vocabListPath,
		numberOfQuestions:        numberOfQuestions,
		serverPort:               serverPort,
		currentQuestion:          1,
		selectedOption:           1,
		appStatus:                enums.Unanswered,
		initialised:              false,
		err:                      nil,
	}

	return m
}
