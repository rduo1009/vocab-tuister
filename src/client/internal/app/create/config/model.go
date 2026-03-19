package config

import (
	"charm.land/huh/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/filepicker"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/jsonview"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util/appdir"
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
	Filepicker    *filepicker.Model
	form          *huh.Form
	jsonview      *jsonview.Model

	// Application state

	AppStatus        createSessionConfigStatus
	FilepickerActive bool
	configFormValues *formValues
	RawSessionConfig string
}

const filepickerID = "configtuiFilepicker"

func New() *Model {
	form, values := defaultForm()

	headerSection := headerSection{focused: false}
	formSection := formSection{focused: false, form: form}
	resetButton := resetButton{focused: false}

	fp := filepicker.New(filepickerID, appdir.AppDirs.UserConfig(), ".json")

	return &Model{
		HeaderSection:    &headerSection,
		FormSection:      &formSection,
		ResetButton:      &resetButton,
		Filepicker:       fp,
		form:             form,
		jsonview:         jsonview.New(""),
		AppStatus:        CreateSessionConfig,
		configFormValues: values,
	}
}
