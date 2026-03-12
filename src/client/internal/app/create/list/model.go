package list

import (
	vocabeditor "github.com/rduo1009/vocab-tuister/src/client/internal/components/vocabeditor/adapter-bubbletea"
)

type createListStatus int

//go:generate go tool stringer -type=createListStatus -linecomment -output=create_list_status_gen.go
const (
	InbuiltList createListStatus = iota // Inbuilt list
	LocalList                           // Local list
	CustomList                          // Create list
)

type (
	headerSection struct{ focused bool }
	selectButton  struct{ focused bool }
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

func (sb *selectButton) Focus() {
	sb.focused = true
}

func (sb *selectButton) Blur() {
	sb.focused = false
}

func (sb *selectButton) Focused() bool {
	return sb.focused
}

type Model struct {
	// Layout state

	width, height int

	// Components

	HeaderSection *headerSection
	VocabEditor   *vocabeditor.Model
	SelectButton  *selectButton

	// Application state

	AppStatus               createListStatus
	inbuiltListDir          string
	vocabEditorInitisalised bool
}

func New(inbuiltListDir string) *Model {
	headerSection := headerSection{focused: false}
	ve := vocabeditor.New(0, 0) // placeholder size values

	ve.DisableInsertMode(true)
	ve.DisableCommandMode(true)
	ve.DisableVisualMode(true)
	ve.DisableVisualLineMode(true)
	ve.DisableSearchMode(true)

	ve.SetCursorMode(vocabeditor.CursorBlink)
	ve.SetLanguage("vocabfile", "catppuccin-mocha") // TODO: Change theme

	selectButton := selectButton{focused: false}

	return &Model{
		HeaderSection:           &headerSection,
		VocabEditor:             &ve,
		SelectButton:            &selectButton,
		AppStatus:               InbuiltList,
		inbuiltListDir:          inbuiltListDir,
		vocabEditorInitisalised: false,
	}
}
