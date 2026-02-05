package list

import (
	vocabeditor "github.com/rduo1009/vocab-tuister/src/client/internal/components/vocabeditor/adapter-bubbletea"
)

type createListStatus int

const (
	InbuiltList createListStatus = iota
	LocalList
	CustomList
)

// NOTE: Manually define the display values.
func (m createListStatus) String() string {
	switch m {
	case InbuiltList:
		return "Inbuilt list"
	case LocalList:
		return "Local list"
	case CustomList:
		return "Create list"
	}
	panic("unreachable")
}

type (
	headerSection struct{ focused bool }
	selectButton  struct{ focused bool }
)

func (hs *headerSection) SetFocused(focused bool) {
	hs.focused = focused
}

func (hs *headerSection) Focused() bool {
	return hs.focused
}

func (hs *headerSection) ID() string {
	return "ListHeaderSection"
}

func (sb *selectButton) SetFocused(focused bool) {
	sb.focused = focused
}

func (sb *selectButton) Focused() bool {
	return sb.focused
}

func (sb *selectButton) ID() string {
	return "SelectButton"
}

type Model struct {
	// Layout state
	width, height int

	// Components
	HeaderSection *headerSection
	VocabEditor   *vocabeditor.Model
	SelectButton  *selectButton

	// Application state
	appStatus               createListStatus
	vocabEditorInitisalised bool
	rawSessionConfig        string
}

func New() *Model {
	headerSection := headerSection{focused: false}
	ve := vocabeditor.New(0, 0) // placeholder size values

	ve.SetInsertMode()
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
		appStatus:               InbuiltList,
		vocabEditorInitisalised: false,
	}
}
