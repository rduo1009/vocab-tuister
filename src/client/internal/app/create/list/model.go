package list

import (
	"fmt"
	"os"

	"github.com/ionut-t/goeditor"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/dropdown"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/filepicker"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/saveas"
	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
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
	editorWrapper struct {
		goeditor.Model
		focused bool
	}
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

func (ew *editorWrapper) Focused() bool {
	return ew.Model.IsFocused()
}

type Model struct {
	// Layout state

	width, height int

	// Components

	HeaderSection *headerSection
	VocabEditor   *editorWrapper
	SelectButton  *selectButton
	ModeDropdown  *dropdown.Model
	Filepicker    *filepicker.Model
	SaveAs        *saveas.Model

	// Application state

	styles             *styles.StylesWrapper
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

func New(inbuiltListDir string, styles *styles.StylesWrapper) *Model {
	headerSection := headerSection{focused: false}
	ed := goeditor.New(0, 0) // placeholder size values

	ed.DisableInsertMode(true)
	ed.DisableCommandMode(true)
	ed.DisableVisualMode(true)
	ed.DisableVisualLineMode(true)
	ed.DisableSearchMode(true)

	ed.SetCursorMode(goeditor.CursorBlink)
	ed.SetLanguage("vocabfile", "bubbletint_vocabeditor")
	ed.WithTheme(styles.Editor.Theme)

	selectButton := selectButton{focused: false}

	modeDropdown := dropdown.New(
		modeDropdownID,
		[]fmt.Stringer{InbuiltList, LocalList, CustomList},
		styles,
	)
	fp := filepicker.New(filepickerID, inbuiltListDir, styles, ".txt")
	homeDir, _ := os.UserHomeDir()
	saveAs := saveas.New(saveAsID, homeDir, styles, ".txt")

	return &Model{
		HeaderSection: &headerSection,
		VocabEditor:   &editorWrapper{Model: ed},
		SelectButton:  &selectButton,

		ModeDropdown: modeDropdown,
		Filepicker:   fp,
		SaveAs:       saveAs,

		styles:         styles,
		AppStatus:      InbuiltList,
		inbuiltListDir: inbuiltListDir,
	}
}
