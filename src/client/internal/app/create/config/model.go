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

func (hs *headerSection) Focus() {
	hs.focused = true
}

func (hs *headerSection) Blur() {
	hs.focused = false
}

func (hs *headerSection) Focused() bool {
	return hs.focused
}

func (fs *formSection) Focus() {
	fs.focused = true
}

func (fs *formSection) Blur() {
	fs.focused = false
}

func (fs *formSection) Focused() bool {
	return fs.focused
}

func (rb *resetButton) Focus() {
	rb.focused = true
}

func (rb *resetButton) Blur() {
	rb.focused = false
}

func (rb *resetButton) Focused() bool {
	return rb.focused
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

	AppStatus        createSessionConfigStatus
	configFormValues *FormValues
	RawSessionConfig string
}

func New() *Model {
	form, values := DefaultForm()

	headerSection := headerSection{focused: false}
	formSection := formSection{focused: false, form: form}
	resetButton := resetButton{focused: false}

	return &Model{
		HeaderSection:    &headerSection,
		FormSection:      &formSection,
		ResetButton:      &resetButton,
		form:             form,
		jsonview:         jsonview.New(""),
		AppStatus:        CreateSessionConfig,
		configFormValues: values,
	}
}
