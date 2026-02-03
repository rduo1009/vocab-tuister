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

	// Application state
	configtuiFilepickerStatus filepickerStatus
	listtuiModeDropdownActive bool
}

func New() *Model {
	configtui := config.New()
	configtuiFilepicker := filepicker.New(appdir.AppDirs.UserConfig(), ".json")
	listtui := list.New()
	listtuiModeDropdown := dropdown.New([]fmt.Stringer{list.InbuiltList, list.LocalList, list.CustomList})

	return &Model{
		configtui:           configtui,
		configtuiFilepicker: configtuiFilepicker,
		listtui:             listtui,
		listtuiModeDropdown: listtuiModeDropdown,

		configtuiFilepickerStatus: filepickerUninitialised,
		listtuiModeDropdownActive: false,
	}
}
