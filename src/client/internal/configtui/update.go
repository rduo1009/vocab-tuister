package configtui

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strconv"

	"github.com/charmbracelet/bubbles/v2/key"
	tea "github.com/charmbracelet/bubbletea/v2"
)

type configMap map[string]any

type (
	errMsg  struct{ err error }
	saveMsg string
)

func squashSettings(wizard SettingsWizard, mcOptionsNumber int) configMap {
	settingsMap := make(configMap)
	for _, page := range wizard.Pages {
		for _, setting := range page.Settings {
			settingsMap[setting.InternalName] = setting.Checked
		}
	}
	settingsMap["number-multiplechoice-options"] = mcOptionsNumber
	return settingsMap
}

func saveConfig(filePath string, config configMap) tea.Cmd {
	return func() tea.Msg {
		absPath, err := filepath.Abs(filePath)
		if err != nil {
			return errMsg{err}
		}

		data, err := json.MarshalIndent(config, "", "  ")
		if err != nil {
			return errMsg{err}
		}

		if err = os.WriteFile(absPath, data, 0o644); err != nil {
			return errMsg{err}
		}

		return saveMsg(absPath)
	}
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd
	var cmd tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		switch {
		case key.Matches(msg, m.keys.Left):
			if m.mcOptionsNumberPage {
				m.mcOptionsNumberPage = false
				break
			}

			if m.currentPage != 0 {
				m.currentPage--
				m.selectedOption = 0
			}

		case key.Matches(msg, m.keys.Right):
			if m.mcOptionsNumberPage {
				value := m.textinput.Value()
				mcOptionsNumber, err := strconv.Atoi(value)
				if err != nil {
					fmt.Printf("Input %s is not a number.", value)
					os.Exit(1)
				}

				return m, saveConfig(m.filePath, squashSettings(m.wizard, mcOptionsNumber))
			}

			if m.currentPage != len(m.wizard.Pages)-1 {
				m.currentPage++
				m.selectedOption = 0
			} else {
				m.mcOptionsNumberPage = true
			}

		case key.Matches(msg, m.keys.Up):
			if !m.mcOptionsNumberPage && m.selectedOption != 0 {
				m.selectedOption--
			}

		case key.Matches(msg, m.keys.Down):
			if !m.mcOptionsNumberPage && m.selectedOption != len(m.wizard.Pages[m.currentPage].Settings)-1 {
				m.selectedOption++
			}

		case key.Matches(msg, m.keys.Check):
			if !m.mcOptionsNumberPage {
				m.toggleSetting(m.currentPage, m.selectedOption)
			}

		case key.Matches(msg, m.keys.Quit):
			return m, tea.Quit
		}

	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height

	case saveMsg:
		return m, tea.Quit

	case errMsg:
		m.err = msg.err
		return m, tea.Quit
	}

	if m.mcOptionsNumberPage {
		m.textinput, cmd = m.textinput.Update(msg)
		cmds = append(cmds, cmd)
	}

	return m, tea.Batch(cmds...)
}
