package root

import (
	"fmt"

	"github.com/charmbracelet/bubbles/v2/help"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/tabs"
	"github.com/rduo1009/vocab-tuister/src/client/internal/types/modes"
	"github.com/rduo1009/vocab-tuister/src/client/internal/types/sessionconfig"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type Model struct {
	// Layout state
	width, height int
	currentPage   int
	pageOrder     []modes.PageName

	// Components
	pages map[modes.PageName]util.ComponentModel
	tabs  *tabs.Tabs
	help  *help.Model // The default help model (used when tabs are focused)

	// Application state
	keys          keyMap
	navigator     *navigator.Navigator
	vocabList     string
	sessionConfig sessionconfig.SessionConfig
	err           error
}

func toStringers[T fmt.Stringer](items []T) []fmt.Stringer {
	res := make([]fmt.Stringer, len(items))
	for i, v := range items {
		res[i] = v
	}
	return res
}

func New() *Model {
	pageOrder := []modes.PageName{
		modes.Create,
		modes.Review,
		modes.Test,
		modes.Help,
		modes.Settings,
	}

	tabs := tabs.New(toStringers(pageOrder), 0, true)
	help := help.New()

	createtui := create.New()

	nav := navigator.New([]navigator.Navigable{}, 0)
	nav.Add(tabs)

	return &Model{
		currentPage: 0,
		pageOrder:   pageOrder,
		pages: map[modes.PageName]util.ComponentModel{
			modes.Create:   createtui,
			modes.Review:   nil,
			modes.Test:     nil,
			modes.Help:     nil,
			modes.Settings: nil,
		}, // TODO: Do this
		tabs:      tabs,
		help:      &help,
		keys:      keys,
		navigator: nav,
	}
}
