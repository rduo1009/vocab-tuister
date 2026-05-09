package create

import (
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/config"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/list"
	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
)

type VerifyStatus int

const (
	StatusMissing VerifyStatus = iota
	StatusPending
	StatusVerified
)

type (
	verifySection struct {
		focused      bool
		ListStatus   VerifyStatus
		ConfigStatus VerifyStatus
	}
)

func (ls *verifySection) Focus() {
	ls.focused = true
}

func (ls *verifySection) Blur() {
	ls.focused = false
}

func (ls *verifySection) Focused() bool {
	return ls.focused
}

func (ls *verifySection) Enabled() bool {
	return ls.ListStatus != StatusMissing && ls.ConfigStatus != StatusMissing
}

type Model struct {
	// Layout state

	width, height int

	// Components

	listtui       *list.Model
	configtui     *config.Model
	VerifySection *verifySection

	// Application state

	styles         *styles.StylesWrapper
	inbuiltListDir string
	serverPort     int
}

func New(inbuiltListDir string, serverPort int, styles *styles.StylesWrapper) *Model {
	listtui := list.New(inbuiltListDir, styles)
	configtui := config.New(styles)
	verifySection := verifySection{focused: false, ListStatus: StatusMissing, ConfigStatus: StatusMissing}

	return &Model{
		listtui:       listtui,
		configtui:     configtui,
		VerifySection: &verifySection,

		styles:         styles,
		inbuiltListDir: inbuiltListDir,
		serverPort:     serverPort,
	}
}
