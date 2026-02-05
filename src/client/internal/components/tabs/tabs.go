package tabs

import (
	"fmt"
	"strings"

	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"
	lipglosscompat "charm.land/lipgloss/v2/compat"
)

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
	highlightColour        = lipglosscompat.AdaptiveColor{Light: lipgloss.Color("#874bfd"), Dark: lipgloss.Color("#7d56f4")}
	highlightFocusedColour = lipglosscompat.AdaptiveColor{Light: lipgloss.Color("#baa8f0"), Dark: lipgloss.Color("#baa8f0")}

	tabGap = inactiveTabStyle(false).
		BorderTop(false).
		BorderLeft(false).
		BorderRight(false)
	tabFocusedGap = inactiveTabStyle(true).
			BorderTop(false).
			BorderLeft(false).
			BorderRight(false)
)

func inactiveTabStyle(focused bool) lipgloss.Style {
	if focused {
		return lipgloss.NewStyle().
			Border(inactiveTabBorder(lipgloss.NormalBorder()), true).
			BorderForeground(highlightFocusedColour).
			Padding(0, 5)
	}
	return lipgloss.NewStyle().
		Border(inactiveTabBorder(lipgloss.NormalBorder()), true).
		BorderForeground(highlightColour).
		Padding(0, 5)
}

func activeTabStyle(focused bool) lipgloss.Style {
	if focused {
		return inactiveTabStyle(focused).Border(activeTabBorder(lipgloss.NormalBorder()), true)
	}
	return inactiveTabStyle(focused).Border(activeTabBorder(lipgloss.NormalBorder()), true)
}

type Model struct {
	Width int

	tabNames  []string
	active    int
	isFocused bool
}

func (t *Model) SetFocused(focused bool) {
	t.isFocused = focused
}

func (t *Model) Focused() bool {
	return t.isFocused
}

func (t *Model) ID() string {
	return "tabs"
}

func (t *Model) Next() {
	t.active++
}

func (t *Model) Prev() {
	t.active--
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
func (t *Model) Init() tea.Cmd {
	return nil
}

// Update helps satisfy the StringViewModel. It is a no-op.
func (t *Model) Update(_ tea.Msg) (*Model, tea.Cmd) {
	return t, nil
}

func (t *Model) View() string {
	// Tabs
	var renderedTabs []string
	for i, pageName := range t.tabNames {
		var style lipgloss.Style
		isActive := i == t.active
		// TODO: Refactor this further after moving styles to styles package.
		if isActive {
			style = activeTabStyle(t.isFocused)
		} else {
			style = inactiveTabStyle(t.isFocused)
		}

		renderedTabs = append(renderedTabs, style.Render(pageName))
	}
	row := lipgloss.JoinHorizontal(lipgloss.Top, renderedTabs...)

	// Gap to the right
	var gap string
	if t.isFocused {
		gap = tabFocusedGap.Render(strings.Repeat(" ", max(0, t.Width-lipgloss.Width(row)-2)))
	} else {
		gap = tabGap.Render(strings.Repeat(" ", max(0, t.Width-lipgloss.Width(row)-2)))
	}

	// Put everything together
	return lipgloss.JoinHorizontal(lipgloss.Bottom, row, gap)
}
