package root

import (
	"charm.land/bubbles/v2/help"
	chromastyles "github.com/alecthomas/chroma/v2/styles"
	tint "github.com/lrstanley/bubbletint/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/create"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/info"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/review"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/root/pages"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/session"
	"github.com/rduo1009/vocab-tuister/src/client/internal/app/settings"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/errordialog"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/tabs"
	pb "github.com/rduo1009/vocab-tuister/src/client/internal/pb/vocab_tuister/v1"
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

	isDark                bool
	hasNerdFonts          bool
	themes                *tint.Registry
	styles                styles.StylesWrapper
	keys                  keyMap
	navigator             *navigator.Navigator
	overlayExpectedActive bool
	vocabList             string
	sessionConfig         *pb.SessionConfig
	numberOfQuestions     int
	err                   error
}

func toTabNames[T tabs.TabName](items []T) []tabs.TabName {
	res := make([]tabs.TabName, len(items))
	for i, v := range items {
		res[i] = v
	}

	return res
}

// TODO: make method currentPageModel() returning m.pages[m.pageOrder[m.currentPage]]

func New(inbuiltListDir string, serverPort int) *Model {
	pageOrder := []pages.PageName{
		pages.Create,
		pages.Review,
		pages.Test,
		pages.Help,
		pages.Settings,
	}

	themes := styles.DefaultThemes(true) // for now, have it be dark

	m := &Model{
		currentPage: 0,
		pageOrder:   pageOrder,
		isDark:      true, // for now as well
		themes:      themes,
		styles: styles.StylesWrapper{
			Styles: styles.DefaultStyles(themes.Current(), false, false), // for now, nerd fonts disabled
		},
	}

	// now everything uses &m.styles
	chromastyles.Register(m.styles.Editor.Chroma)

	m.tabs = tabs.New(toTabNames(pageOrder), 0, true, &m.styles)

	h := help.New()
	overlayHelp := help.New()

	createtui := create.New(inbuiltListDir, serverPort, &m.styles)
	reviewtui := review.New(&m.styles)

	sessiontui := session.New(
		&createtui.VerifySection.ListStatus,
		&createtui.VerifySection.ConfigStatus,
		serverPort,
		&m.vocabList,
		&m.sessionConfig,
		&m.numberOfQuestions,
		&m.styles,
	)

	infotui := info.New(&m.styles)
	settingstui := settings.New(&m.styles)

	m.pages = map[pages.PageName]app.PageModel{
		pages.Create:   createtui,
		pages.Review:   reviewtui,
		pages.Test:     sessiontui,
		pages.Help:     infotui,
		pages.Settings: settingstui,
	}

	nav := navigator.New([]navigator.Navigable{}, 0)
	nav.Add(m.tabs)

	m.navigator = nav
	m.help = &h
	m.overlayHelp = &overlayHelp
	m.keys = keys
	m.errorDialog = errordialog.New(&m.styles)

	return m
}
