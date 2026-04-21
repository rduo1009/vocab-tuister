package jsonview

import (
	"bytes"
	"strings"

	"charm.land/bubbles/v2/help"
	"charm.land/bubbles/v2/key"
	"charm.land/bubbles/v2/viewport"
	tea "charm.land/bubbletea/v2"
	"github.com/alecthomas/chroma/v2/quick"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
)

// Model is a bubbletea component that displays JSON content with syntax highlighting
// and scrolling capabilities. It uses the viewport component for scrolling and
// the chroma library for syntax highlighting.
type Model struct {
	// viewport is the underlying viewport that handles scrolling
	viewport viewport.Model
	// content is the raw JSON string to display
	content string
	// highlighted is the cached syntax-highlighted version of the content
	highlighted string
	// keys contains the keybindings for navigation
}

// New creates a new JSON viewer component with the given JSON content.
// The viewport must be sized using SetWidth and SetHeight before use.
func New(jsonContent string) *Model {
	// Create a new viewport without initial dimensions
	vp := viewport.New()

	return &Model{
		content:  jsonContent,
		viewport: vp,
	}
}

// Init initializes the component. It returns nil as no initial commands
// are needed for this component.
func (m *Model) Init() tea.Cmd {
	return nil
}

// Update handles incoming messages and updates the component state accordingly.
// It delegates all message handling to the viewport, which handles navigation
// keys internally. The method returns the updated model and any commands to execute.
func (m *Model) Update(msg tea.Msg) (app.ComponentModel, tea.Cmd) {
	// Delegate all message handling to the viewport
	// The viewport handles navigation keys (arrows, page up/down, etc.) internally
	var cmd tea.Cmd

	m.viewport, cmd = m.viewport.Update(msg)

	return m, cmd
}

// View renders the component as a string. It returns the viewport's view.
func (m *Model) View() string {
	return m.viewport.View()
}

// SetWidth sets the width of the component and updates the viewport accordingly.
// This also refreshes the content to ensure it's properly formatted for the new width.
func (m *Model) SetWidth(width int) {
	m.viewport.SetWidth(width)
	// Refresh content with the new width
	m.viewport.SetContent(m.getHighlightedContent())
}

// SetHeight sets the height of the component and updates the viewport accordingly.
// This also refreshes the content to ensure it's properly formatted for the new height.
func (m *Model) SetHeight(height int) {
	m.viewport.SetHeight(height)
	// Refresh content with the new height
	m.viewport.SetContent(m.getHighlightedContent())
}

type jsonViewKeyMap struct {
	parent *viewport.KeyMap
}

// ShortHelp returns keybindings for the mini help view.
func (k jsonViewKeyMap) ShortHelp() []key.Binding {
	return []key.Binding{
		k.parent.Up,
		k.parent.Down,
		k.parent.PageUp,
		k.parent.PageDown,
	}
}

// FullHelp returns keybindings for the expanded help view.
func (k jsonViewKeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.parent.Up, k.parent.Down, k.parent.PageUp, k.parent.PageDown},
		{k.parent.HalfPageUp, k.parent.HalfPageDown},
		{k.parent.Left, k.parent.Right},
	}
}

// KeyMap returns the component's keymap for help display.
// It implements part of the ComponentModel interface.
func (m *Model) KeyMap() help.KeyMap {
	return jsonViewKeyMap{&m.viewport.KeyMap}
}

// SetContent updates the JSON content displayed by the component.
// It clears the highlighted cache and resets the scroll position to the top.
func (m *Model) SetContent(jsonContent string) {
	m.content = jsonContent
	// Clear the cache so it gets regenerated with the new content
	m.highlighted = ""
	// Update the viewport with the new content
	m.viewport.SetContent(m.getHighlightedContent())
	// Reset to top when content changes
	m.viewport.GotoTop()
}

// getHighlightedContent returns the syntax-highlighted version of the JSON content.
// It caches the result to avoid re-highlighting on every render. The highlighting
// uses the chroma library with the terminal256 formatter and monokai theme.
// If highlighting fails, it falls back to the plain content.
func (m *Model) getHighlightedContent() string {
	// Return cached version if available
	if m.highlighted != "" {
		return m.highlighted
	}

	// Use chroma to syntax highlight the JSON
	var buf bytes.Buffer

	// err := quick.Highlight(&buf, m.content, "json", "terminal256", "bubbletint_json")
	err := quick.Highlight(&buf, m.content, "json", "terminal256", "catppuccin-mocha")
	if err != nil {
		// If highlighting fails for any reason, fall back to plain text
		// This ensures the component is resilient to highlighting errors
		m.highlighted = m.content
		return m.content
	}

	// Cache the highlighted output, removing any trailing newline
	highlighted := buf.String()
	m.highlighted = strings.TrimSuffix(highlighted, "\n")

	return m.highlighted
}
