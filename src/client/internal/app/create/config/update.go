package config

import (
	"encoding/json/jsontext"
	"encoding/json/v2"
	"fmt"
	"os"
	"strconv"

	"charm.land/bubbles/v2/key"
	tea "charm.land/bubbletea/v2"
	"charm.land/huh/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/filepicker"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type configMap map[string]any

type (
	rawSessionConfigMsg []byte

	// In case there is an error with `generateSessionConfig` to distinguish with `app.ErrMsg`.
	failFormMsg struct{}
)

func generateSessionConfig(values *ConfigFormValues) tea.Cmd {
	generate := func() ([]byte, error) {
		configMap := make(configMap)

		allSelections := [][]string{
			values.PartsOfSpeechExclusions,
			values.VerbExclusions,
			values.ParticipleExclusions,
			values.OtherVerbExclusions,
			values.NounExclusions,
			values.AdjectiveExclusions,
			values.AdverbExclusions,
			values.PronounExclusions,
			values.RegularExclusions,
			values.Miscellaneous,
			values.QuestionTypes,
		}

		selected := make(map[string]struct{})
		for _, selections := range allSelections {
			for _, key := range selections {
				selected[key] = struct{}{}
			}
		}

		for _, key := range allKeys {
			_, ok := selected[key]
			configMap[key] = ok
		}

		numberMultipleChoiceOptions, err := strconv.Atoi(values.NumberMultipleChoiceOptionsString)
		if err != nil {
			return nil, fmt.Errorf(
				"failed to convert %s to integer: %w",
				values.NumberMultipleChoiceOptionsString,
				err,
			)
		}

		configMap["number-multiplechoice-options"] = numberMultipleChoiceOptions

		numberOfQuestions, err := strconv.Atoi(values.NumberOfQuestionsString)
		if err != nil {
			return nil, fmt.Errorf(
				"failed to convert %s to integer: %w",
				values.NumberOfQuestionsString,
				err,
			)
		}

		configMap["number-of-questions"] = numberOfQuestions

		data, err := json.Marshal(configMap)
		if err != nil {
			return nil, fmt.Errorf("failed to marshal session config: %w", err)
		}

		// Convert to Value and canonicalize to maintain alphabetical key ordering
		value := jsontext.Value(data)

		err = value.Canonicalize(
			jsontext.WithIndent("  "),
			jsontext.SpaceAfterColon(true),
			jsontext.SpaceAfterComma(false),
		)
		if err != nil {
			return nil, fmt.Errorf("failed to canonicalize json: %w", err)
		}

		return value, nil
	}

	rawSessionConfig, err := generate()
	if err != nil {
		return tea.Batch(util.MsgCmd(app.ErrMsg(err)), util.MsgCmd(failFormMsg{}))
	}

	return util.MsgCmd(rawSessionConfigMsg(rawSessionConfig))
}

func readSessionConfigFile(selectedFile string) tea.Cmd {
	return func() tea.Msg {
		rawSessionConfig, err := os.ReadFile(selectedFile)
		if err != nil {
			return app.ErrMsg(fmt.Errorf("failed to read session config file at %s: %w", selectedFile, err))
		}

		value := jsontext.Value(rawSessionConfig)

		err = value.Canonicalize(jsontext.WithIndent("  "),
			jsontext.SpaceAfterColon(true),
			jsontext.SpaceAfterComma(false),
		)
		if err != nil {
			return app.ErrMsg(fmt.Errorf("failed to canonicalize json: %w", err))
		}

		return rawSessionConfigMsg(value)
	}
}

func (m *Model) Update(msg tea.Msg) (app.ComponentModel, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		if m.HeaderSection.Focused() && key.Matches(msg, m.HeaderSection.KeyMap().PressButton) {
			cmds = append(cmds, util.MsgCmd(filepicker.StartMsg{ID: "configtuiFilepicker"}))
		} else if m.ResetButton.Focused() && key.Matches(msg, m.ResetButton.KeyMap().PressButton) {
			m.form, m.configFormValues = DefaultForm()
			m.form.State = huh.StateNormal
			m.appStatus = CreateSessionConfig
			m.RawSessionConfig = ""
			cmds = append(cmds, util.MsgCmd(navigator.RemoveNavigableMsg{
				IDs: []string{m.ResetButton.ID()},
			}))
		}

	case rawSessionConfigMsg:
		m.appStatus = ReviewSessionConfig
		m.RawSessionConfig = string(msg)
		m.jsonview.SetContent(m.RawSessionConfig)

		// navigator: [..., HeaderSection, FormSection, ...]
		cmds = append(cmds,
			// now navigator: [..., HeaderSection, ResetButton, FormSection, ...]
			util.MsgCmd(navigator.ReplaceNavigableMsg{
				ID:         m.FormSection.ID(),
				Components: []navigator.Navigable{m.ResetButton, m.FormSection},
			}),
			util.MsgCmd(navigator.FocusNavigableMsg{ID: m.FormSection.ID()}),
		)

		// NOTE: use tea.Sequence as these need to be ran in order
		// also note that `cmds` could not be altered after this, so returning early is fine
		return m, tea.Sequence(cmds...)

	case filepicker.PickedMsg:
		if msg.ID == "configtuiFilepicker" {
			cmds = append(cmds, readSessionConfigFile(msg.SelectedFile))
		}

	case failFormMsg:
		m.form, m.configFormValues = DefaultForm()
		m.form.State = huh.StateNormal
		m.appStatus = CreateSessionConfig
		m.RawSessionConfig = ""
		cmds = append(cmds, util.MsgCmd(navigator.RemoveNavigableMsg{
			IDs: []string{m.ResetButton.ID()},
		}))
	}

	if m.FormSection.Focused() {
		switch m.form.State {
		case huh.StateNormal:
			util.UpdaterPtr(&cmds, m.form, msg)

		case huh.StateCompleted:
			switch m.appStatus {
			case CreateSessionConfig: // i.e. the form has just been finished
				cmds = append(cmds, generateSessionConfig(m.configFormValues))

			case ReviewSessionConfig:
				util.UpdaterPtr(&cmds, m.jsonview, msg)
			}
		}
	}

	return m, tea.Batch(cmds...)
}
