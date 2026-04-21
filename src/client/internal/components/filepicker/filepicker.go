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

	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type (
	StartMsg   struct{ ID string }
	ExitMsg    struct{ ID string }
	SetPathMsg struct {
		ID   string
		Path string
	}
	PickedMsg struct {
		ID           string
		SelectedFile string
	}
)

type clearErrorMsg struct{}

func clearErrorAfter(t time.Duration) tea.Cmd {
	return tea.Tick(t, func(_ time.Time) tea.Msg {
		return clearErrorMsg{}
	})
}

type Model struct {
	ID            string
	width, height int
	keys          filePickerKeys

	filepicker filepicker.Model
	help       help.Model

	styles       *styles.StylesWrapper
	selectedFile string
	err          error
}

type filePickerKeys struct {
	filepicker.KeyMap
	Submit key.Binding
	Help   key.Binding
	Exit   key.Binding
	Quit   key.Binding
}

func (k filePickerKeys) ShortHelp() []key.Binding {
	return []key.Binding{k.Up, k.Down, k.Open, k.Back, k.Submit, k.Help, k.Exit, k.Quit}
}

func (k filePickerKeys) FullHelp() [][]key.Binding {
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

func New(id, currentDirectory string, styles *styles.StylesWrapper, allowedTypes ...string) *Model {
	fp := filepicker.New()
	fp.Styles = styles.Filepicker

	help := help.New()

	if len(allowedTypes) > 0 {
		fp.AllowedTypes = allowedTypes
	}

	if currentDirectory != "" {
		fp.CurrentDirectory = currentDirectory
	}

	keys := filePickerKeys{
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

	return &Model{ID: id, filepicker: fp, help: help, keys: keys, styles: styles}
}

func (m *Model) Init() tea.Cmd {
	return m.filepicker.Init()
}

func (m *Model) SetPath(path string) {
	m.filepicker.CurrentDirectory = path
}

func (m *Model) Update(msg tea.Msg) (*Model, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case SetPathMsg:
		if msg.ID == m.ID {
			m.filepicker.CurrentDirectory = msg.Path
			m.selectedFile = ""
			m.err = nil
			cmds = append(cmds, m.filepicker.Init())
		}

	case tea.KeyPressMsg:
		switch {
		case key.Matches(msg, m.keys.Submit):
			if m.selectedFile == "" {
				m.err = errors.New("cannot submit as no file was selected")

				cmds = append(cmds, clearErrorAfter(2*time.Second))
			} else {
				cmds = append(cmds, util.MsgCmd(PickedMsg{
					ID:           m.ID,
					SelectedFile: m.selectedFile,
				}))
			}

		case key.Matches(msg, m.keys.Help):
			m.help.ShowAll = !m.help.ShowAll

		case key.Matches(msg, m.keys.Exit):
			cmds = append(cmds, util.MsgCmd(ExitMsg{ID: m.ID}))
			return m, tea.Batch(cmds...) // or else the filepicker's own esc handling will run
		}

	case clearErrorMsg:
		m.err = nil
	}

	util.UpdaterVal(&cmds, &m.filepicker, msg)
	util.UpdaterVal(&cmds, &m.help, msg)

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

		m.err = fmt.Errorf("%s is not valid (expected %s)", path, expected)
		m.selectedFile = ""

		cmds = append(cmds, clearErrorAfter(2*time.Second))
	}

	return m, tea.Batch(cmds...)
}

func (m *Model) SetWidth(width int) {
	m.width = width
}

func (m *Model) SetHeight(height int) {
	m.height = height
}

func (m *Model) View(screenWidth, screenHeight int) (view string, x, y int) {
	m.filepicker.SetHeight(m.height)
	m.filepicker.Styles.EmptyDirectory = m.filepicker.Styles.EmptyDirectory.SetString(
		"No files found in directory.",
	)

	var b strings.Builder

	switch {
	case m.err != nil:
		b.WriteString(m.styles.Error.Render(m.err.Error()))

	case m.selectedFile == "":
		fmt.Fprintf(&b, "Pick a file (in %s):", m.filepicker.CurrentDirectory)

	default:
		b.WriteString("Selected file: " + m.filepicker.Styles.Selected.Render(m.selectedFile))
	}

	b.WriteString("\n\n")
	b.WriteString(m.filepicker.View())

	content := b.String()
	help := m.help.View(m.keys)

	view = m.styles.OverlayBorder.
		Padding(0, 1).
		Width(m.width).
		Height(m.height).
		Render(lipgloss.JoinVertical(lipgloss.Left, content, help))
	x = (screenWidth - lipgloss.Width(view)) / 2
	y = (screenHeight - lipgloss.Height(view)) / 2

	return view, x, y
}
