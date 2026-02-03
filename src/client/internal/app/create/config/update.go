package config

import (
	"encoding/json/jsontext"
	"encoding/json/v2"
	"fmt"
	"os"
	"strconv"

	"github.com/charmbracelet/bubbles/v2/key"
	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/huh/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/filepicker"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type configMap map[string]any

type RawSessionConfigMsg []byte

func generateSessionConfig() tea.Msg {
	configMap := make(configMap)

	allSelections := [][]string{
		partsOfSpeechExclusions,
		verbExclusions,
		participleExclusions,
		otherVerbExclusions,
		nounExclusions,
		adjectiveExclusions,
		adverbExclusions,
		pronounExclusions,
		regularExclusions,
		miscellaneous,
		questionTypes,
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
	numberMultipleChoiceOptionsString, err := strconv.Atoi(numberMultipleChoiceOptions)
	if err != nil {
		return app.ErrMsg(fmt.Errorf("failed to convert %s to integer: %w", numberMultipleChoiceOptions, err))
	}
	configMap["number-multiplechoice-options"] = numberMultipleChoiceOptionsString

	numberOfQuestionsString, err := strconv.Atoi(numberOfQuestions)
	if err != nil {
		return app.ErrMsg(fmt.Errorf("failed to convert %s to integer: %w", numberOfQuestions, err))
	}
	configMap["number-of-questions"] = numberOfQuestionsString

	data, err := json.Marshal(configMap)
	if err != nil {
		return app.ErrMsg(fmt.Errorf("failed to marshal session config: %w", err))
	}

	// Convert to Value and canonicalize to maintain alphabetical key ordering
	var value jsontext.Value = data
	err = value.Canonicalize(
		jsontext.WithIndent("  "),
		jsontext.SpaceAfterColon(true),
		jsontext.SpaceAfterComma(false),
	)
	if err != nil {
		return app.ErrMsg(fmt.Errorf("failed to canonicalize json: %w", err))
	}

	return RawSessionConfigMsg(value)
}

func readSessionConfigFile(selectedFile string) tea.Cmd {
	return func() tea.Msg {
		rawSessionConfig, err := os.ReadFile(selectedFile)
		if err != nil {
			return app.ErrMsg(fmt.Errorf("failed to read session config file at %s: %w", selectedFile, err))
		}

		var value jsontext.Value = rawSessionConfig
		err = value.Canonicalize(jsontext.WithIndent("  "),
			jsontext.SpaceAfterColon(true),
			jsontext.SpaceAfterComma(false),
		)
		if err != nil {
			return app.ErrMsg(fmt.Errorf("failed to canonicalize json: %w", err))
		}

		return RawSessionConfigMsg(value)
	}
}

func (m *Model) Update(msg tea.Msg) (util.ComponentModel, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		if m.HeaderSection.Focused() {
			switch {
			case key.Matches(msg, m.HeaderSection.KeyMap().PressButton):
				cmds = append(cmds, util.MsgCmd(filepicker.FilepickStartMsg{}))
			}
		} else if m.ResetButton.Focused() {
			switch {
			case key.Matches(msg, m.ResetButton.KeyMap().PressButton):
				m.form = DefaultForm()
				m.form.State = huh.StateNormal
				m.appStatus = CreateSessionConfig
				cmds = append(cmds, util.MsgCmd(navigator.RemoveNavigableMsg{
					IDs: []string{m.ResetButton.ID()},
				}))
			}
		}

	case RawSessionConfigMsg:
		m.appStatus = ReviewSessionConfig
		m.rawSessionConfig = string(msg)
		m.jsonview.SetContent(m.rawSessionConfig)

	case filepicker.FilepickPickedMsg:
		cmds = append(cmds, readSessionConfigFile(msg.SelectedFile))
	}

	if m.FormSection.Focused() {
		switch m.form.State {
		case huh.StateNormal:
			_, cmd := m.form.Update(msg)
			cmds = append(cmds, cmd)
		case huh.StateCompleted:
			switch m.appStatus {
			case CreateSessionConfig: // i.e. the form has just been finished
				// navigator: [HeaderSection, FormSection]
				cmds = append(cmds, generateSessionConfig,
					// now navigator: [HeaderSection]
					util.MsgCmd(navigator.RemoveNavigableMsg{
						IDs: []string{m.FormSection.ID()},
					}),
					// now navigator: [HeaderSection, ResetButton, FormSection]
					util.MsgCmd(navigator.AddNavigableMsg{
						Components: []navigator.Navigable{m.ResetButton, m.FormSection},
					}),
				)
				// NOTE: use tea.Sequence as these need to be ran in order
				// also note that `cmds` could not be altered after this, so returning early is fine
				return m, tea.Sequence(cmds...)
			case ReviewSessionConfig:
				_, cmd := m.jsonview.Update(msg)
				cmds = append(cmds, cmd)
			}
		}
	}

	return m, tea.Batch(cmds...)
}
