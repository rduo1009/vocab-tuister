package session

import (
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questioncomponents"
	pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"
	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
)

type (
	returnButton  struct{ focused bool }
	restartButton struct{ focused bool }
)

func (rtb *returnButton) Focus() {
	rtb.focused = true
}

func (rtb *returnButton) Blur() {
	rtb.focused = false
}

func (rtb *returnButton) Focused() bool {
	return rtb.focused
}

func (rsb *restartButton) Focus() {
	rsb.focused = true
}

func (rsb *restartButton) Blur() {
	rsb.focused = false
}

func (rsb *restartButton) Focused() bool {
	return rsb.focused
}

type testingSessionStatus int

const (
	Unavailable testingSessionStatus = iota
	Uninitialised
	Initialised
	Completed
)

type Model struct {
	// Layout state

	width, height int

	// Components

	questionProvider     QuestionProvider
	currentQuestionModel questioncomponents.QuestionModel
	returnButton         *returnButton
	restartButton        *restartButton

	// Application state

	styles         *styles.StylesWrapper
	listVerified   *create.VerifyStatus
	configVerified *create.VerifyStatus

	answeredCount       int // number of questions that have been answered
	correctCount        int // number of questions that were answered correctly
	dropdownActive      bool
	activeDropdownIndex int
	serverPort          int
	vocabList           *string
	sessionConfig       **pb.SessionConfig
	numberOfQuestions   *int
	appStatus           testingSessionStatus
}

func New(
	listVerified, configVerified *create.VerifyStatus,
	serverPort int,
	vocabList *string,
	sessionConfig **pb.SessionConfig,
	numberOfQuestions *int,
	styles *styles.StylesWrapper,
) *Model {
	return &Model{
		returnButton:      &returnButton{},
		restartButton:     &restartButton{},
		styles:            styles,
		listVerified:      listVerified,
		configVerified:    configVerified,
		serverPort:        serverPort,
		vocabList:         vocabList,
		sessionConfig:     sessionConfig,
		numberOfQuestions: numberOfQuestions,
		appStatus:         Unavailable,
	}
}
