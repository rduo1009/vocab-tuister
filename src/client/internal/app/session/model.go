package session

import (
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session/questioncomponents"
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

	questions     []questioncomponents.QuestionModel
	returnButton  *returnButton
	restartButton *restartButton

	// Application state

	listLoaded   *create.LoadStatus
	configLoaded *create.LoadStatus

	// index of the current question
	currentIndex int
	// total number of questions
	questionCount int
	// number of questions that have been answered
	answeredCount int
	// number of questions that were answered correctly
	correctCount        int
	dropdownActive      bool
	activeDropdownIndex int
	serverPort          int
	appStatus           testingSessionStatus
}

func New(listLoaded, configLoaded *create.LoadStatus, serverPort int) *Model {
	return &Model{
		returnButton:  &returnButton{},
		restartButton: &restartButton{},
		listLoaded:    listLoaded,
		configLoaded:  configLoaded,
		serverPort:    serverPort,
		appStatus:     Unavailable,
	}
}
