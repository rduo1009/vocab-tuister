package create

import (
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/config"
)

type Model struct {
	// Layout state
	width, height int

	// Components
	configtui *config.Model

	// Application state
	err error
}

func New() *Model {
	configtui := config.New()
	return &Model{configtui: configtui}
}
