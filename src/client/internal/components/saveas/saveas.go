package saveas

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"charm.land/bubbles/v2/filepicker"
	"charm.land/bubbles/v2/help"
	"charm.land/bubbles/v2/key"
	"charm.land/bubbles/v2/textinput"
	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type (
	StartMsg    struct{ ID string }
	ExitMsg     struct{ ID string }
	SelectedMsg struct {
		ID        string
		Path      string
		Overwrite bool
	}
	SetPathMsg struct {
		ID   string
		Path string
	}
)

type Model struct {
	ID            string
	width, height int
	keys          saveAsKeys

	filepicker filepicker.Model
	textinput  textinput.Model
	help       help.Model

	confirmOverwrite bool
	pendingPath      string
	err              error
}

type saveAsKeys struct {
	filepicker.KeyMap
	Submit     key.Binding
	CycleFocus key.Binding
	Help       key.Binding
	Exit       key.Binding
}

func (k saveAsKeys) ShortHelp() []key.Binding {
	return []key.Binding{k.CycleFocus, k.Submit, k.Help, k.Exit}
}

func (k saveAsKeys) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.CycleFocus, k.Submit},
		{k.Up, k.Down, k.Open, k.Back},
		{k.Help, k.Exit},
	}
}

func (m *Model) KeyMap() help.KeyMap {
	return m.keys
}

func New(id, currentDirectory string, allowedTypes ...string) *Model {
	fp := filepicker.New()

	fp.CurrentDirectory = currentDirectory
	if len(allowedTypes) > 0 {
		fp.AllowedTypes = allowedTypes
	}

	ti := textinput.New()
	ti.Placeholder = "Enter filename..."
	ti.Blur()

	hlp := help.New()

	keys := saveAsKeys{
		KeyMap: filepicker.DefaultKeyMap(),
		Submit: key.NewBinding(
			key.WithKeys("enter"),
			key.WithHelp("enter", "submit"),
		),
		CycleFocus: key.NewBinding(
			key.WithKeys("tab", "shift+tab", "[", "]"),
			key.WithHelp("tab/[]", "cycle focus"),
		),
		Help: key.NewBinding(
			key.WithKeys("ctrl+h"),
			key.WithHelp("ctrl+h", "toggle help"),
		),
		Exit: key.NewBinding(
			key.WithKeys("esc"),
			key.WithHelp("esc", "cancel"),
		),
	}

	return &Model{
		ID:         id,
		filepicker: fp,
		textinput:  ti,
		help:       hlp,
		keys:       keys,
	}
}

func (m *Model) Init() tea.Cmd {
	return tea.Batch(m.filepicker.Init(), textinput.Blink)
}

func (m *Model) Update(msg tea.Msg) (*Model, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case SetPathMsg:
		if msg.ID == m.ID {
			m.filepicker.CurrentDirectory = msg.Path
			m.err = nil
			// cmds = append(cmds, m.filepicker.Init())
		}

	case tea.KeyPressMsg:
		// 1. Handle Overwrite Confirmation Mode
		if m.confirmOverwrite {
			switch msg.String() {
			case "y", "Y", "enter":
				// Confirm overwrite
				cmds = append(cmds, util.MsgCmd(SelectedMsg{
					ID:        m.ID,
					Path:      m.pendingPath,
					Overwrite: true,
				}))
				m.confirmOverwrite = false
				m.pendingPath = ""

			case "n", "N", "esc":
				// Cancel overwrite
				m.confirmOverwrite = false
				m.pendingPath = ""
			}

			return m, nil // Consume key
		}

		// 2. Handle Global Navigation (Focus Switching & Exit)

		if key.Matches(msg, m.keys.CycleFocus) {
			if m.textinput.Focused() {
				m.textinput.Blur()
			} else {
				cmds = append(cmds, m.textinput.Focus())
			}

			return m, tea.Batch(cmds...)
		}

		if key.Matches(msg, m.keys.Exit) {
			cmds = append(cmds, util.MsgCmd(ExitMsg{ID: m.ID}))
			return m, tea.Batch(cmds...)
		}

		if key.Matches(msg, m.keys.Help) {
			m.help.ShowAll = !m.help.ShowAll
			return m, nil
		}

		// 3. Handle Component-Specific Logic
		if m.textinput.Focused() {
			if key.Matches(msg, m.keys.Submit) {
				// Attempt to submit
				filename := strings.TrimSpace(m.textinput.Value())
				if filename == "" {
					m.err = errors.New("filename cannot be empty")

					cmds = append(cmds, clearErrorAfter(2*time.Second))

					return m, tea.Batch(cmds...)
				}

				if len(m.filepicker.AllowedTypes) > 0 {
					valid := false

					for _, ext := range m.filepicker.AllowedTypes {
						if strings.HasSuffix(filename, ext) {
							valid = true
							break
						}
					}

					if !valid {
						m.err = fmt.Errorf(
							"invalid file type (expected %s)",
							strings.Join(m.filepicker.AllowedTypes, ", "),
						)

						cmds = append(cmds, clearErrorAfter(2*time.Second))

						return m, tea.Batch(cmds...)
					}
				}

				fullPath := filepath.Join(m.filepicker.CurrentDirectory, filename)

				// Check for existence
				if _, err := os.Stat(fullPath); err == nil {
					// File exists -> Ask for overwrite
					m.confirmOverwrite = true
					m.pendingPath = fullPath
				} else {
					// File doesn't exist -> Select immediately
					cmds = append(cmds, util.MsgCmd(SelectedMsg{
						ID:        m.ID,
						Path:      fullPath,
						Overwrite: false,
					}))
				}

				return m, tea.Batch(cmds...)
			}
		}

	case clearErrorMsg:
		m.err = nil
	}

	// 4. Update Components
	// Always update textinput (it respects its own focus)
	util.UpdaterVal(&cmds, &m.textinput, msg)

	// Always update filepicker to keep it fresh, BUT block key events if not focused
	// to prevent accidental navigation while typing.
	// Bubbles filepicker doesn't have a "Focus" boolean, so we filter messages.
	if !m.textinput.Focused() {
		util.UpdaterVal(&cmds, &m.filepicker, msg)
		util.UpdaterVal(&cmds, &m.help, msg)

		// If filepicker selected a file (e.g. user hit Enter on a file),
		// we might want to populate textinput with that filename.
		if didSelect, path := m.filepicker.DidSelectFile(msg); didSelect {
			m.textinput.SetValue(filepath.Base(path))
			cmds = append(cmds, m.textinput.Focus())
		}

		// Handle disabled file selection
		if didSelect, path := m.filepicker.DidSelectDisabledFile(msg); didSelect {
			expected := "valid file type"
			if len(m.filepicker.AllowedTypes) > 0 {
				expected = "file ending in " + strings.Join(m.filepicker.AllowedTypes, ", ")
			}

			m.err = fmt.Errorf("%s is not valid (expected %s)", filepath.Base(path), expected)

			cmds = append(cmds, clearErrorAfter(2*time.Second))
		}
	} else {
		// Even if not focused, we might want to update filepicker for non-key messages
		// (like window resize, or async file loading if it had any).
		// However, we must filter out KeyPressMsg.
		if _, ok := msg.(tea.KeyPressMsg); !ok {
			util.UpdaterVal(&cmds, &m.filepicker, msg)
		}
	}

	return m, tea.Batch(cmds...)
}

type clearErrorMsg struct{}

func clearErrorAfter(t time.Duration) tea.Cmd {
	return tea.Tick(t, func(_ time.Time) tea.Msg {
		return clearErrorMsg{}
	})
}

var (
	errorStyle  = lipgloss.NewStyle().Foreground(lipgloss.Color("#fa003f"))
	borderStyle = lipgloss.NewStyle().Border(lipgloss.RoundedBorder()).Padding(0, 1)
	dimStyle    = lipgloss.NewStyle().Faint(true)

	overlayBoxStyle = lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			Padding(1, 2).
			BorderForeground(lipgloss.Color("63")) // Purple-ish border
	warnOverlayStyle = lipgloss.NewStyle().Foreground(lipgloss.Color("202")).Bold(true) // Orange/Red warning
)

func (m *Model) SetWidth(width int) {
	m.width = width
}

func (m *Model) SetHeight(height int) {
	m.height = height
}

func (m *Model) View(screenWidth, screenHeight int) (string, int, int) {
	// --- Construction of Base View ---

	// 1. Header
	header := "Save in: " + m.filepicker.CurrentDirectory
	if m.err != nil {
		header = errorStyle.Render(m.err.Error())
	}

	// 2. File Picker
	// Calculate available height for file picker
	// Total Height - Header(1) - "Filename:"(1) - TextInput(1) - Borders(2) = approx -5?
	fpHeight := max(m.height-6, 5) // 5 is minimum viable height
	m.filepicker.SetHeight(fpHeight)

	fpStyle := lipgloss.NewStyle().Border(lipgloss.NormalBorder())
	if !m.textinput.Focused() {
		fpStyle = fpStyle.BorderForeground(lipgloss.Color("63"))
	} else {
		fpStyle = fpStyle.BorderForeground(lipgloss.Color("240")) // Dim border
	}

	fpView := fpStyle.Width(m.width - 4).Render(m.filepicker.View()) // -4 for paddings/borders

	// 3. Text Input
	tiStyle := lipgloss.NewStyle()
	if m.textinput.Focused() {
		tiStyle = tiStyle.Foreground(lipgloss.Color("63"))
	} else {
		tiStyle = tiStyle.Foreground(lipgloss.Color("240"))
	}

	tiView := tiStyle.Render(m.textinput.View())

	// Assemble Base Stack
	content := lipgloss.JoinVertical(lipgloss.Left,
		header,
		fpView,
		"Filename:",
		tiView,
	)

	// Add Help view
	helpView := m.help.View(m.keys)
	fullView := borderStyle.Width(m.width).
		Height(m.height).
		Render(lipgloss.JoinVertical(lipgloss.Left, content, helpView))

	var finalView string

	// --- Compositor for Overlay ---

	if m.confirmOverwrite {
		// Layer 0: Dimmed Base
		dimLayer := lipgloss.NewLayer(dimStyle.Render(fullView))

		// Layer 1: Centered Overlay
		overwriteText := fmt.Sprintf(
			"%s\n\nFile %s already exists.\nOverwrite? (y/n)",
			warnOverlayStyle.Render("WARNING"),
			filepath.Base(m.pendingPath),
		)
		overlayContent := overlayBoxStyle.Render(overwriteText)

		// Center the overlay content within the full view dimensions
		// lipgloss.Place creates a string of size w x h with content placed inside
		centeredOverlay := lipgloss.Place(
			m.width, m.height,
			lipgloss.Center, lipgloss.Center,
			overlayContent,
		)

		overlayLayer := lipgloss.NewLayer(centeredOverlay)

		finalView = lipgloss.NewCompositor(dimLayer, overlayLayer).Render()
	} else {
		finalView = fullView
	}

	x := (screenWidth - lipgloss.Width(finalView)) / 2
	y := (screenHeight - lipgloss.Height(finalView)) / 2

	return finalView, x, y
}
