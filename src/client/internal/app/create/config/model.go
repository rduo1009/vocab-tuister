package config

import (
	"charm.land/huh/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/jsonview"
)

type createSessionConfigStatus int

const (
	CreateSessionConfig createSessionConfigStatus = iota
	ReviewSessionConfig
)

type (
	headerSection struct{ focused bool }
	formSection   struct {
		focused bool
		form    *huh.Form
	}
	resetButton struct{ focused bool }
)

func (hs *headerSection) SetFocused(focused bool) {
	hs.focused = focused
}

func (hs *headerSection) Focused() bool {
	return hs.focused
}

func (hs *headerSection) ID() string {
	return "ConfigHeaderSection"
}

func (fs *formSection) SetFocused(focused bool) {
	fs.focused = focused
}

func (fs *formSection) Focused() bool {
	return fs.focused
}

func (fs *formSection) ID() string {
	return "FormSection"
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
	HeaderSection *headerSection
	FormSection   *formSection
	ResetButton   *resetButton
	form          *huh.Form
	jsonview      *jsonview.Model

	// Application state
	appStatus        createSessionConfigStatus
	RawSessionConfig string
}

func New() *Model {
	form := DefaultForm()

	headerSection := headerSection{focused: false}
	formSection := formSection{focused: false, form: form}
	resetButton := resetButton{focused: false}

	return &Model{
		HeaderSection: &headerSection,
		FormSection:   &formSection,
		ResetButton:   &resetButton,
		form:          form,
		jsonview:      jsonview.New(""),
		appStatus:     CreateSessionConfig,
	}
}
