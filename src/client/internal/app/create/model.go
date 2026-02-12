package create

import (
	"fmt"
	"os"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/config"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/list"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/dropdown"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/filepicker"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/saveas"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util/appdir"
)

type loadStatus int

const (
	StatusMissing loadStatus = iota
	StatusPending
	StatusLoaded
)

type (
	loadSection struct {
		focused      bool
		ListStatus   loadStatus
		ConfigStatus loadStatus
	}
)

func (ls *loadSection) SetFocused(focused bool) {
	ls.focused = focused
}

func (ls *loadSection) Focused() bool {
	return ls.focused
}

func (ls *loadSection) ID() string {
	return "LoadSection"
}

func (ls *loadSection) Enabled() bool {
	return ls.ListStatus == StatusPending && ls.ConfigStatus == StatusPending
}

type Model struct {
	// Layout state
	width, height int

	// Components
	listtui             *list.Model
	listtuiModeDropdown *dropdown.Model
	listtuiFilepicker   *filepicker.Model
	listtuiSaveAs       *saveas.Model
	configtui           *config.Model
	configtuiFilepicker *filepicker.Model
	LoadSection         *loadSection

	// Application state
	listtuiModeDropdownActive bool
	listtuiFilepickerActive   bool
	listtuiSaveAsActive       bool
	inbuiltListDir            string
	configtuiFilepickerActive bool
}

func New(inbuiltListDir string) *Model {
	listtui := list.New(inbuiltListDir)
	listtuiModeDropdown := dropdown.New([]fmt.Stringer{list.InbuiltList, list.LocalList, list.CustomList})
	listtuiFilepicker := filepicker.New("listtuiFilepicker", inbuiltListDir, ".txt")
	homeDir, _ := os.UserHomeDir()
	listtuiSaveAs := saveas.New("listtuiSaveAs", homeDir, ".txt")

	configtui := config.New()
	configtuiFilepicker := filepicker.New("configtuiFilepicker", appdir.AppDirs.UserConfig(), ".json")

	loadSection := loadSection{focused: false, ListStatus: StatusMissing, ConfigStatus: StatusMissing}

	return &Model{
		listtui:             listtui,
		listtuiModeDropdown: listtuiModeDropdown,
		listtuiFilepicker:   listtuiFilepicker,
		listtuiSaveAs:       listtuiSaveAs,

		configtui:           configtui,
		configtuiFilepicker: configtuiFilepicker,

		LoadSection: &loadSection,

		configtuiFilepickerActive: false,
		listtuiModeDropdownActive: false,
		listtuiFilepickerActive:   false,
		listtuiSaveAsActive:       false,
		inbuiltListDir:            inbuiltListDir,
	}
}
