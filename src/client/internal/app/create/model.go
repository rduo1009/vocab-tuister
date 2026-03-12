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

type LoadStatus int

const (
	StatusMissing LoadStatus = iota
	StatusPending
	StatusLoaded
)

type (
	loadSection struct {
		focused      bool
		ListStatus   LoadStatus
		ConfigStatus LoadStatus
	}
)

func (ls *loadSection) Focus() {
	ls.focused = true
}

func (ls *loadSection) Blur() {
	ls.focused = false
}

func (ls *loadSection) Focused() bool {
	return ls.focused
}

func (ls *loadSection) Enabled() bool {
	return ls.ListStatus != StatusMissing && ls.ConfigStatus != StatusMissing
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
	serverPort                int
	configtuiFilepickerActive bool
}

func New(inbuiltListDir string, serverPort int) *Model {
	listtui := list.New(inbuiltListDir)
	listtuiModeDropdown := dropdown.New(
		"listtuiDropdown",
		[]fmt.Stringer{list.InbuiltList, list.LocalList, list.CustomList},
	)
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
		serverPort:                serverPort,
	}
}
