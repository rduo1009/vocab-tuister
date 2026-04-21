package root

import (
	"fmt"

	"charm.land/bubbles/v2/help"
	chromastyles "github.com/alecthomas/chroma/v2/styles"
	tint "github.com/lrstanley/bubbletint/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create/config/sessionconfig"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/info"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/review"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/root/pages"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/settings"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/errordialog"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/tabs"
	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
)

type Model struct {
	// Layout state

	width, height int
	currentPage   int
	pageOrder     []pages.PageName

	// Components

	pages       map[pages.PageName]app.PageModel
	tabs        *tabs.Model
	help        *help.Model
	overlayHelp *help.Model
	errorDialog errordialog.Model

	// Application state

	themes        *tint.Registry
	styles        styles.StylesWrapper
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

func New(inbuiltListDir string, serverPort int) *Model {
	pageOrder := []pages.PageName{
		pages.Create,
		pages.Review,
		pages.Test,
		pages.Help,
		pages.Settings,
	}

	themes := styles.DefaultThemes()
	s := styles.StylesWrapper{Styles: styles.DefaultStyles(themes.Current())}
	chromastyles.Register(s.Editor.Chroma)
	chromastyles.Register(s.Jsonview)

	t := tabs.New(toStringers(pageOrder), 0, true, &s)
	h := help.New()
	overlayHelp := help.New()

	createtui := create.New(inbuiltListDir, serverPort, &s)
	reviewtui := review.New(&s)
	// unfortunately sessiontui needs to be coupled with createtui
	// to prevent user from starting session without loading list + config
	sessiontui := session.New(
		&createtui.LoadSection.ListStatus,
		&createtui.LoadSection.ConfigStatus,
		serverPort,
		&s,
	)
	infotui := info.New(&s)
	settingstui := settings.New(&s)

	nav := navigator.New([]navigator.Navigable{}, 0)
	nav.Add(t)

	return &Model{
		currentPage: 0,
		pageOrder:   pageOrder,
		pages: map[pages.PageName]app.PageModel{
			pages.Create:   createtui,
			pages.Review:   reviewtui,
			pages.Test:     sessiontui,
			pages.Help:     infotui,
			pages.Settings: settingstui,
		},
		themes:      themes,
		styles:      s,
		tabs:        t,
		help:        &h,
		overlayHelp: &overlayHelp,
		keys:        keys,
		navigator:   nav,
		errorDialog: errordialog.New(&s),
	}
}
