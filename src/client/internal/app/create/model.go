package create

import (
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/config"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/list"
	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
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

	styles         *styles.StylesWrapper
	inbuiltListDir string
	serverPort     int
}

func New(inbuiltListDir string, serverPort int, styles *styles.StylesWrapper) *Model {
	listtui := list.New(inbuiltListDir, styles)
	configtui := config.New(styles)
	loadSection := loadSection{focused: false, ListStatus: StatusMissing, ConfigStatus: StatusMissing}

	return &Model{
		listtui:     listtui,
		configtui:   configtui,
		LoadSection: &loadSection,

		styles:         styles,
		inbuiltListDir: inbuiltListDir,
		serverPort:     serverPort,
	}
}
