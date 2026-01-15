package dropdown

import (
	"fmt"
	"io"

	"github.com/charmbracelet/bubbles/v2/help"
	"github.com/charmbracelet/bubbles/v2/list"
	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

const (
	defaultWidth = 20
	listHeight   = 6 // XXX: ??
)

var (
	itemStyle         = lipgloss.NewStyle().Background(lipgloss.Color("#707070"))
	selectedItemStyle = lipgloss.NewStyle().Background(lipgloss.Color("#a7a7a7"))
	quitTextStyle     = lipgloss.NewStyle().Margin(1, 0, 2, 4)
)

type item string

func (i item) FilterValue() string { return "" }

type itemDelegate struct{}

func (d itemDelegate) Height() int                             { return 1 }
func (d itemDelegate) Spacing() int                            { return 0 }
func (d itemDelegate) Update(_ tea.Msg, _ *list.Model) tea.Cmd { return nil }
func (d itemDelegate) Render(w io.Writer, m list.Model, index int, listItem list.Item) {
	i, ok := listItem.(item)
	if !ok {
		return
	}

	str := fmt.Sprintf("%s", i)

	var fn func(...string) string
	if index == m.Index() {
		fn = selectedItemStyle.Width(m.Width()).Render
	} else {
		fn = itemStyle.Width(m.Width()).Render
	}

	fmt.Fprint(w, fn(str))
}

type Model struct {
	width, height int
	list          list.Model
	choice        string
	quitting      bool
}

// TODO: Use?
//
//	AdditionalShortHelpKeys func() []key.Binding
//	AdditionalFullHelpKeys  func() []key.Binding
func New(names []string) *Model {
	var items []list.Item
	for _, name := range names {
		items = append(items, item(name))
	}

	l := list.New(items, itemDelegate{}, defaultWidth, listHeight)
	l.SetShowTitle(false)
	l.SetShowStatusBar(false)
	l.SetFilteringEnabled(false)
	l.SetShowPagination(false)

	m := &Model{list: l}
	m.width = defaultWidth
	m.height = listHeight // TODO: remove later
	return m
}

func (m *Model) Init() tea.Cmd {
	return nil
}

func (m *Model) Update(msg tea.Msg) (util.ComponentModel, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch keypress := msg.String(); keypress {
		case "enter":
			i, ok := m.list.SelectedItem().(item)
			if ok {
				m.choice = string(i)
			}
			return m, tea.Quit
		}
	}

	var cmd tea.Cmd
	m.list, cmd = m.list.Update(msg)
	return m, cmd
}

func (m *Model) SetWidth(width int) {
	m.width = width
}

func (m *Model) SetHeight(height int) {
	m.height = height
}

func (m *Model) View() string {
	m.list.SetWidth(m.width)
	m.list.SetHeight(m.height)
	return "\n" + m.list.View()
}

func (m *Model) KeyMap() help.KeyMap {
	return m.list
}
