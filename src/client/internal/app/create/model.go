package create

import (
	"fmt"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/config"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/list"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/dropdown"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/filepicker"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util/appdir"
)

type filepickerStatus int

const (
	filepickerUninitialised filepickerStatus = iota
	filepickerInactive
	filepickerActive
)

type Model struct {
	// Layout state
	width, height int

	// Components
	configtui           *config.Model
	configtuiFilepicker *filepicker.Model
	listtui             *list.Model
	listtuiModeDropdown *dropdown.Model
	listtuiFilepicker   *filepicker.Model

	// Application state
	configtuiFilepickerStatus filepickerStatus
	listtuiFilepickerStatus   filepickerStatus
	listtuiModeDropdownActive bool
	inbuiltListDir            string
}

func New(inbuiltListDir string) *Model {
	configtui := config.New()
	configtuiFilepicker := filepicker.New("configtuiFilepicker", appdir.AppDirs.UserConfig(), ".json")
	listtui := list.New(inbuiltListDir)
	listtuiModeDropdown := dropdown.New([]fmt.Stringer{list.InbuiltList, list.LocalList, list.CustomList})
	listtuiFilepicker := filepicker.New("listtuiFilepicker", inbuiltListDir, ".txt")

	return &Model{
		configtui:           configtui,
		configtuiFilepicker: configtuiFilepicker,
		listtui:             listtui,
		listtuiModeDropdown: listtuiModeDropdown,
		listtuiFilepicker:   listtuiFilepicker,

		configtuiFilepickerStatus: filepickerUninitialised,
		listtuiFilepickerStatus:   filepickerUninitialised,
		listtuiModeDropdownActive: false,
		inbuiltListDir:            inbuiltListDir,
	}
}
