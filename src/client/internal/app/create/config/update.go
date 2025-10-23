package config

import (
	"encoding/json/jsontext"
	"encoding/json/v2"

	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/huh/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/types/modes"
	"github.com/rduo1009/vocab-tuister/src/client/internal/types/sessionconfig"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type configMap map[string]any

type (
	errMsg           struct{ err error }
	sessionConfigMsg struct{ sessionConfig sessionconfig.SessionConfig }
)

func generateSessionConfig(form *huh.Form) tea.Cmd {
	return func() tea.Msg {
		for _, page := range wizard.Pages {
			for _, option := range page.Options {
				switch option.Type {
				case modes.OptionBool:
					option.BoolValue = form.GetBool(option.InternalName)
				case modes.OptionNumber:
					option.NumberValue = form.GetInt(option.InternalName)
				}
			}
		}

		configMap := make(configMap)
		for _, page := range wizard.Pages {
			for _, option := range page.Options {
				switch option.Type {
				case modes.OptionBool:
					configMap[option.InternalName] = option.BoolValue
				case modes.OptionNumber:
					configMap[option.InternalName] = option.NumberValue
				}
			}
		}

		var sessionConfig sessionconfig.SessionConfig

		data, err := json.Marshal(configMap)
		if err != nil {
			return errMsg{err}
		}

		// Convert to Value and canonicalize to maintain alphabetical key ordering
		var value jsontext.Value = data
		err = value.Canonicalize(
			jsontext.WithIndent("  "),
			jsontext.SpaceAfterColon(true),
			jsontext.SpaceAfterComma(false),
		)
		if err != nil {
			return errMsg{err}
		}

		json.Unmarshal(value, &sessionConfig)

		return sessionConfigMsg{sessionConfig}
	}
}

func (m *Model) Update(msg tea.Msg) (util.ComponentModel, tea.Cmd) {
	var cmds []tea.Cmd
	var cmd tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyMsg:
		if m.HeaderBorder.Focused() {
			switch {
			}
		} else {
			_, cmd = m.form.Update(msg)
			cmds = append(cmds, cmd)
		}

	// case reset_button_was_touched:
	// 	m.form = newForm()

	case errMsg:
		m.err = msg.err
		return m, tea.Quit
	}

	if m.form.State == huh.StateCompleted { // XXX: Will this run too many times?
		if m.appStatus == CreateSessionConfig {
			m.appStatus = ReviewSessionConfig
			cmds = append(cmds, generateSessionConfig(m.form))
		}
	}

	return m, tea.Batch(cmds...)
}
