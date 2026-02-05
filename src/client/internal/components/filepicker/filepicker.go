package filepicker

import (
	"errors"
	"fmt"
	"strings"
	"time"

	"charm.land/bubbles/v2/filepicker"
	"charm.land/bubbles/v2/help"
	"charm.land/bubbles/v2/key"
	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type (
	FilepickStartMsg  struct{}
	FilepickExitMsg   struct{}
	FilepickPickedMsg struct{ SelectedFile string }
)

type clearErrorMsg struct{}

func clearErrorAfter(t time.Duration) tea.Cmd {
	return tea.Tick(t, func(_ time.Time) tea.Msg {
		return clearErrorMsg{}
	})
}

type Model struct {
	Height int
	Width  int
	keys   FilePickerKeys

	filepicker filepicker.Model

	selectedFile string
	err          error
}

type FilePickerKeys struct {
	filepicker.KeyMap
	Submit key.Binding
	Help   key.Binding
	Exit   key.Binding
	Quit   key.Binding
}

func (k FilePickerKeys) ShortHelp() []key.Binding {
	return []key.Binding{k.Up, k.Down, k.Open, k.Back, k.Submit, k.Help, k.Exit, k.Quit}
}

func (k FilePickerKeys) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.GoToTop, k.GoToLast},
		{k.Up, k.Down, k.PageUp, k.PageDown},
		{k.Open, k.Select, k.Back},
		{k.Submit, k.Help, k.Exit, k.Quit},
	}
}

func (m *Model) KeyMap() help.KeyMap {
	return m.keys
}

func New(currentDirectory string, allowedTypes ...string) *Model {
	fp := filepicker.New()

	if len(allowedTypes) > 0 {
		fp.AllowedTypes = allowedTypes
	}
	if currentDirectory != "" {
		fp.CurrentDirectory = currentDirectory
	}

	keys := FilePickerKeys{
		KeyMap: filepicker.DefaultKeyMap(),
		Submit: key.NewBinding(
			key.WithKeys("ctrl+s"),
			key.WithHelp("ctrl+s", "submit"),
		),
		Help: key.NewBinding(
			key.WithKeys("ctrl+h"),
			key.WithHelp("ctrl+h", "toggle additional help"),
		),
		Exit: key.NewBinding(
			key.WithKeys("esc"),
			key.WithHelp("esc", "cancel"),
		),
		Quit: key.NewBinding(
			key.WithKeys("ctrl+q", "ctrl+c"),
			key.WithHelp("ctrl+q", "quit"),
		),
	}
	return &Model{filepicker: fp, keys: keys}
}

func (m *Model) Init() tea.Cmd {
	return m.filepicker.Init()
}

func (m *Model) Update(msg tea.Msg) (*Model, tea.Cmd) {
	var cmds []tea.Cmd
	var cmd tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		switch {
		case key.Matches(msg, m.keys.Submit):
			if m.selectedFile == "" {
				m.err = errors.New("Cannot submit as no file was selected")
				cmds = append(cmds, clearErrorAfter(2*time.Second))
			} else {
				cmds = append(cmds, util.MsgCmd(FilepickPickedMsg{
					SelectedFile: m.selectedFile,
				}))
			}
		case key.Matches(msg, m.keys.Exit):
			cmds = append(cmds, util.MsgCmd(FilepickExitMsg{}))
		}

	case clearErrorMsg:
		m.err = nil
	}

	m.filepicker, cmd = m.filepicker.Update(msg)
	cmds = append(cmds, cmd)

	// Did the user select a file?
	if didSelect, path := m.filepicker.DidSelectFile(msg); didSelect {
		// Get the path of the selected file.
		m.selectedFile = path
	}

	// Did the user select a disabled file?
	// This is only necessary to display an error to the user.
	if didSelect, path := m.filepicker.DidSelectDisabledFile(msg); didSelect {
		// Let's clear the selectedFile and display an error.
		expected := "valid file type"
		if len(m.filepicker.AllowedTypes) > 0 {
			expected = "file ending in " + strings.Join(m.filepicker.AllowedTypes, ", ")
		}

		m.err = errors.New(path + " is not valid (expected " + expected + ")")
		m.selectedFile = ""
		cmds = append(cmds, clearErrorAfter(2*time.Second))
	}

	return m, tea.Batch(cmds...)
}

var errorStyle = lipgloss.NewStyle().Foreground(lipgloss.Color("#fa003f"))

func (m *Model) View() string {
	m.filepicker.SetHeight(m.Height)
	m.filepicker.Styles.EmptyDirectory = m.filepicker.Styles.EmptyDirectory.SetString("No files found in directory.")

	var b strings.Builder
	if m.err != nil {
		b.WriteString(errorStyle.Render(m.err.Error()))
	} else if m.selectedFile == "" {
		b.WriteString(fmt.Sprintf("Pick a file (in %s):", m.filepicker.CurrentDirectory))
	} else {
		b.WriteString("Selected file: " + m.filepicker.Styles.Selected.Render(m.selectedFile))
	}
	b.WriteString("\n\n")
	b.WriteString(m.filepicker.View())

	return b.String()
}
