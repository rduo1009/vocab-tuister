package list

import (
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/dropdown"
	vocabeditor "github.com/rduo1009/vocab-tuister/src/client/internal/components/vocabeditor/adapter-bubbletea"
)

type createListStatus int

const (
	InbuiltList createListStatus = iota
	LocalList
	CustomList
)

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
	ModeDropdown  *dropdown.Model
	VocabEditor   *vocabeditor.Model
	SelectButton  *selectButton

	// Application state
	appStatus            createListStatus
	statusDropdownActive bool
	rawSessionConfig     string
}

func New() *Model {
	headerSection := headerSection{focused: false}
	modeDropdown := dropdown.New([]string{"Inbuilt list", "Local list", "Create list"})
	ve := vocabeditor.New(0, 0) // placeholder size values
	selectButton := selectButton{focused: false}

	return &Model{
		HeaderSection: &headerSection,
		ModeDropdown:  modeDropdown,
		VocabEditor:   &ve,
		SelectButton:  &selectButton,
		appStatus:     InbuiltList,
	}
}
