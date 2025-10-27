package create

import (
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/config"
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

	// Application state
	configtuiFilepickerStatus filepickerStatus
}

func New() *Model {
	configtui := config.New()
	configtuiFilepicker := filepicker.New(appdir.AppDirs.UserConfig(), ".json")

	return &Model{configtui: configtui, configtuiFilepicker: configtuiFilepicker, configtuiFilepickerStatus: filepickerUninitialised}
}
