package config

import (
	"github.com/charmbracelet/bubbles/v2/help"
	"github.com/charmbracelet/huh/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/types/modes"
)

type appStatus int

const (
	CreateSessionConfig appStatus = iota
	ReviewSessionConfig
)

type (
	headerBorder struct{ focused bool }
	formBorder   struct {
		focused bool
		form    *huh.Form
	}
)

func (hb *headerBorder) SetFocused(focused bool) {
	hb.focused = focused
}

func (hb *headerBorder) Focused() bool {
	return hb.focused
}

func (fb *formBorder) SetFocused(focused bool) {
	fb.focused = focused
}

func (fb *formBorder) Focused() bool {
	return fb.focused
}

type Model struct {
	// Layout state
	width, height int

	// Components
	HeaderBorder *headerBorder
	FormBorder   *formBorder
	form         *huh.Form
	help         *help.Model // The default help model (used when selecting preset is focused)

	// Application state
	appStatus appStatus
	keys      keyMap
	wizard    *SessionConfigWizard
	err       error

	filePath string
}

// NOTE: This doesn't reset SettingsWizard. The values in SettingsWizard should remain the same.
func newForm() *huh.Form {
	groups := make([]*huh.Group, len(wizard.Pages))
	for i, page := range wizard.Pages {
		if page.Options[0].Type == modes.OptionBool {
			groups[i] = huh.NewGroup(
				huh.NewMultiSelect[string]().
					Title(page.Title).
					Options(func() (o []huh.Option[string]) {
						for _, field := range page.Options {
							o = append(
								o,
								huh.NewOption(field.DisplayName, field.InternalName).
									Selected(field.BoolValue),
							)
						}
						return o
					}()...),
			)
			continue
		}

		options := make([]huh.Field, len(page.Options))
		for j, option := range page.Options {
			switch option.Type {
			case modes.OptionNumber:
				options[j] = huh.NewInput().Title(option.DisplayName).Prompt(">")

			default:
				panic("unreachable")
			}
		}

		groups[i] = huh.NewGroup(options...)
	}

	return huh.NewForm(groups...)
}

func New() *Model {
	form := newForm()  // returns pointer
	help := help.New() // returns value

	headerBorder := headerBorder{focused: false}
	formBorder := formBorder{focused: false, form: form}

	return &Model{
		HeaderBorder: &headerBorder,
		FormBorder:   &formBorder,
		form:         form,
		help:         &help,
		appStatus:    CreateSessionConfig,
		keys:         headerKeys,
		wizard:       &wizard,
	}
}
