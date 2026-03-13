package create

import (
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/config"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/list"
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

	listtui     *list.Model
	configtui   *config.Model
	LoadSection *loadSection

	// Application state

	inbuiltListDir string
	serverPort     int
}

func New(inbuiltListDir string, serverPort int) *Model {
	listtui := list.New(inbuiltListDir)
	configtui := config.New()
	loadSection := loadSection{focused: false, ListStatus: StatusMissing, ConfigStatus: StatusMissing}

	return &Model{
		listtui:     listtui,
		configtui:   configtui,
		LoadSection: &loadSection,

		inbuiltListDir: inbuiltListDir,
		serverPort:     serverPort,
	}
}
