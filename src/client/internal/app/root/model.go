package root

import (
	"fmt"

	"charm.land/bubbles/v2/help"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/review"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/errordialog"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/tabs"
	"github.com/rduo1009/vocab-tuister/src/client/internal/types/modes"
	"github.com/rduo1009/vocab-tuister/src/client/internal/types/sessionconfig"
)

type Model struct {
	// Layout state

	width, height int
	currentPage   int
	pageOrder     []modes.PageName

	// Components

	pages       map[modes.PageName]app.PageModel
	tabs        *tabs.Model
	help        *help.Model
	overlayHelp *help.Model
	errorDialog errordialog.Model

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

func New(inbuiltListDir string) *Model {
	pageOrder := []modes.PageName{
		modes.Create,
		modes.Review,
		modes.Test,
		modes.Help,
		modes.Settings,
	}

	t := tabs.New(toStringers(pageOrder), 0, true)
	h := help.New()
	overlayHelp := help.New()

	createtui := create.New(inbuiltListDir)
	reviewtui := review.New()
	// unfortunately sessiontui needs to be coupled with createtui
	// to prevent user from starting session without loading list + config
	sessiontui := session.New(&createtui.LoadSection.ListStatus, &createtui.LoadSection.ConfigStatus)

	nav := navigator.New([]navigator.Navigable{}, 0)
	nav.Add(t)

	return &Model{
		currentPage: 0,
		pageOrder:   pageOrder,
		pages: map[modes.PageName]app.PageModel{
			modes.Create:   createtui,
			modes.Review:   reviewtui,
			modes.Test:     sessiontui,
			modes.Help:     nil,
			modes.Settings: nil,
		},
		tabs:        t,
		help:        &h,
		overlayHelp: &overlayHelp,
		keys:        keys,
		navigator:   nav,
		errorDialog: errordialog.New(),
	}
}
