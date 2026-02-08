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

type Model struct {
	// Layout state
	width, height int

	// Components
	configtui           *config.Model
	configtuiFilepicker *filepicker.Model
	listtui             *list.Model
	listtuiModeDropdown *dropdown.Model
	listtuiFilepicker   *filepicker.Model
	listtuiSaveAs       *saveas.Model

	// Application state
	configtuiFilepickerActive bool
	listtuiModeDropdownActive bool
	listtuiFilepickerActive   bool
	listtuiSaveAsActive       bool
	inbuiltListDir            string
}

func New(inbuiltListDir string) *Model {
	configtui := config.New()
	configtuiFilepicker := filepicker.New("configtuiFilepicker", appdir.AppDirs.UserConfig(), ".json")
	listtui := list.New(inbuiltListDir)
	listtuiModeDropdown := dropdown.New([]fmt.Stringer{list.InbuiltList, list.LocalList, list.CustomList})
	listtuiFilepicker := filepicker.New("listtuiFilepicker", inbuiltListDir, ".txt")

	homeDir, _ := os.UserHomeDir()
	listtuiSaveAs := saveas.New("listtuiSaveAs", homeDir, ".txt")

	return &Model{
		configtui:           configtui,
		configtuiFilepicker: configtuiFilepicker,
		listtui:             listtui,
		listtuiModeDropdown: listtuiModeDropdown,
		listtuiFilepicker:   listtuiFilepicker,
		listtuiSaveAs:       listtuiSaveAs,

		configtuiFilepickerActive: false,
		listtuiModeDropdownActive: false,
		listtuiFilepickerActive:   false,
		listtuiSaveAsActive:       false,
		inbuiltListDir:            inbuiltListDir,
	}
}
