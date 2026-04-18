package tabs

import (
	"fmt"
	"strings"

	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
)

type SelectTabMsg struct{ Index int }

type Model struct {
	Width int

	tabNames  []string
	active    int
	isFocused bool

	styles *styles.StylesWrapper
}

func (m *Model) Focus() {
	m.isFocused = true
}

func (m *Model) Blur() {
	m.isFocused = false
}

func (m *Model) Focused() bool {
	return m.isFocused
}

func (m *Model) Next() {
	m.active++
}

func (m *Model) Prev() {
	m.active--
}

func (m *Model) Select(index int) {
	m.active = index
}

func New(names []fmt.Stringer, active int, isFocused bool, styles *styles.StylesWrapper) *Model {
	tabNames := make([]string, len(names))
	for i, n := range names {
		tabNames[i] = n.String()
	}

	return &Model{
		tabNames:  tabNames,
		active:    active,
		isFocused: isFocused,
		styles:    styles,
	}
}

// Init helps satisfy the StringViewModel. It is a no-op.
func (m *Model) Init() tea.Cmd {
	return nil
}

// Update helps satisfy the StringViewModel. It is a no-op.
func (m *Model) Update(_ tea.Msg) (*Model, tea.Cmd) {
	return m, nil
}

func (m *Model) View() string {
	// Determine padding width
	// NOTE: crazy vibe-coded magic. still works though
	textWidth := 0
	for _, name := range m.tabNames {
		textWidth += lipgloss.Width(name)
	}

	borderWidth := 2 * len(m.tabNames)

	targetWidth := m.Width / 2
	remaining := targetWidth - textWidth - borderWidth

	pad := 1
	if remaining > 0 {
		pad = max(1, (remaining+(len(m.tabNames)*2-1))/(len(m.tabNames)*2))
	}

	if pad > 5 {
		pad = 5
	}

	// Tabs
	var renderedTabs []string
	for i, pageName := range m.tabNames {
		style := m.styles.TabBorder(i == m.active, m.isFocused, pad)

		renderedTabs = append(renderedTabs, style.Render(pageName))
	}

	row := lipgloss.JoinHorizontal(lipgloss.Top, renderedTabs...)

	// Gap to the right
	var gap string

	remainingGap := max(0, m.Width-lipgloss.Width(row)-2)
	gap = m.styles.TabGap(m.isFocused).Render(strings.Repeat(" ", remainingGap))

	// Put everything together
	return lipgloss.JoinHorizontal(lipgloss.Bottom, row, gap)
}
