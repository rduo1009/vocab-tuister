package tabs

import (
	"fmt"
	"strings"

	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"
	lipglosscompat "charm.land/lipgloss/v2/compat"
)

type SelectTabMsg struct{ Index int }

func inactiveTabBorder(b lipgloss.Border) lipgloss.Border {
	b.Top = "─"
	b.Bottom = "─"
	b.Left = "│"
	b.Right = "│"
	b.TopLeft = "╭"
	b.TopRight = "╮"
	b.BottomLeft = "┴"
	b.BottomRight = "┴"

	return b
}

func activeTabBorder(b lipgloss.Border) lipgloss.Border {
	b.Top = "─"
	b.Bottom = " "
	b.Left = "│"
	b.Right = "│"
	b.TopLeft = "╭"
	b.TopRight = "╮"
	b.BottomLeft = "┘"
	b.BottomRight = "└"

	return b
}

var (
	// TODO: Remove need to use lipglosscompat.
	highlightColour = lipglosscompat.AdaptiveColor{
		Light: lipgloss.Color("#874bfd"),
		Dark:  lipgloss.Color("#7d56f4"),
	}
	highlightFocusedColour = lipglosscompat.AdaptiveColor{
		Light: lipgloss.Color("#baa8f0"),
		Dark:  lipgloss.Color("#baa8f0"),
	}
)

func tabGap(focused bool) lipgloss.Style {
	return inactiveTabStyle(focused, 0).
		BorderTop(false).
		BorderLeft(false).
		BorderRight(false)
}

func inactiveTabStyle(focused bool, pad int) lipgloss.Style {
	if focused {
		return lipgloss.NewStyle().
			Border(inactiveTabBorder(lipgloss.NormalBorder()), true).
			BorderForeground(highlightFocusedColour).
			Padding(0, pad)
	}

	return lipgloss.NewStyle().
		Border(inactiveTabBorder(lipgloss.NormalBorder()), true).
		BorderForeground(highlightColour).
		Padding(0, pad)
}

func activeTabStyle(focused bool, pad int) lipgloss.Style {
	if focused {
		return lipgloss.NewStyle().
			Border(activeTabBorder(lipgloss.NormalBorder()), true).
			BorderForeground(highlightFocusedColour).
			Padding(0, pad)
	}

	return lipgloss.NewStyle().
		Border(activeTabBorder(lipgloss.NormalBorder()), true).
		BorderForeground(highlightColour).
		Padding(0, pad)
}

type Model struct {
	Width int

	tabNames  []string
	active    int
	isFocused bool
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

func New(names []fmt.Stringer, active int, isFocused bool) *Model {
	tabNames := make([]string, len(names))
	for i, n := range names {
		tabNames[i] = n.String()
	}

	return &Model{
		tabNames:  tabNames,
		active:    active,
		isFocused: isFocused,
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
		var style lipgloss.Style

		isActive := i == m.active
		// TODO: Refactor this further after moving styles to styles package.
		if isActive {
			style = activeTabStyle(m.isFocused, pad)
		} else {
			style = inactiveTabStyle(m.isFocused, pad)
		}

		renderedTabs = append(renderedTabs, style.Render(pageName))
	}

	row := lipgloss.JoinHorizontal(lipgloss.Top, renderedTabs...)

	// Gap to the right
	var gap string

	remainingGap := max(0, m.Width-lipgloss.Width(row)-2)
	gap = tabGap(m.isFocused).Render(strings.Repeat(" ", remainingGap))

	// Put everything together
	return lipgloss.JoinHorizontal(lipgloss.Bottom, row, gap)
}
