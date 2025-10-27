package config

import (
	"github.com/charmbracelet/huh/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/jsonview"
)

type appStatus int

const (
	CreateSessionConfig appStatus = iota
	ReviewSessionConfig
)

type (
	headerBorder struct{ focused bool }
	formBorder   struct {
		focused bool
		form    *huh.Form
	}
	resetButton struct{ focused bool }
)

func (hb *headerBorder) SetFocused(focused bool) {
	hb.focused = focused
}

func (hb *headerBorder) Focused() bool {
	return hb.focused
}

func (hb *headerBorder) ID() string {
	return "HeaderBorder"
}

func (fb *formBorder) SetFocused(focused bool) {
	fb.focused = focused
}

func (fb *formBorder) Focused() bool {
	return fb.focused
}

func (fb *formBorder) ID() string {
	return "FormBorder"
}

func (rb *resetButton) SetFocused(focused bool) {
	rb.focused = focused
}

func (rb *resetButton) Focused() bool {
	return rb.focused
}

func (rb *resetButton) ID() string {
	return "ResetButton"
}

type Model struct {
	// Layout state
	width, height int

	// Components
	HeaderSection *headerBorder
	FormSection   *formBorder
	ResetButton   *resetButton
	form          *huh.Form
	jsonview      *jsonview.Model

	// Application state
	appStatus        appStatus
	rawSessionConfig string
}

func New() *Model {
	form := DefaultForm()

	headerBorder := headerBorder{focused: false}
	formBorder := formBorder{focused: false, form: form}
	resetButton := resetButton{focused: false}

	return &Model{
		HeaderSection: &headerBorder,
		FormSection:   &formBorder,
		ResetButton:   &resetButton,
		form:          form,
		jsonview:      jsonview.New(""),
		appStatus:     CreateSessionConfig,
	}
}
