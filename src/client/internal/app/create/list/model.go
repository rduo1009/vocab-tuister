package list

import (
	"fmt"
	"os"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/dropdown"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/filepicker"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/saveas"
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
	ModeDropdown  *dropdown.Model
	Filepicker    *filepicker.Model
	SaveAs        *saveas.Model

	// Application state

	AppStatus          createListStatus
	FilepickerActive   bool
	ModeDropdownActive bool
	SaveAsActive       bool
	inbuiltListDir     string
}

const (
	filepickerID   = "listtuiFilepicker"
	modeDropdownID = "listtuiDropdown"
	saveAsID       = "listtuiSaveAs"
)

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

	modeDropdown := dropdown.New(
		modeDropdownID,
		[]fmt.Stringer{InbuiltList, LocalList, CustomList},
	)
	fp := filepicker.New(filepickerID, inbuiltListDir, ".txt")
	homeDir, _ := os.UserHomeDir()
	saveAs := saveas.New(saveAsID, homeDir, ".txt")

	return &Model{
		HeaderSection: &headerSection,
		VocabEditor:   &ve,
		SelectButton:  &selectButton,

		ModeDropdown:   modeDropdown,
		Filepicker:     fp,
		SaveAs:         saveAs,
		AppStatus:      InbuiltList,
		inbuiltListDir: inbuiltListDir,
	}
}
