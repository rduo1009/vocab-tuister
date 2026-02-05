package dropdown

import (
	"fmt"
	"io"

	"charm.land/bubbles/v2/help"
	"charm.land/bubbles/v2/list"
	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type (
	DropdownStartMsg  struct{}
	DropdownExitMsg   struct{}
	DropdownPickedMsg struct{ ChosenItem fmt.Stringer }
)

const (
	defaultWidth = 20
	listHeight   = 6 // XXX: Choose value
)

var (
	itemStyle         = lipgloss.NewStyle().Background(lipgloss.Color("#707070"))
	selectedItemStyle = lipgloss.NewStyle().Background(lipgloss.Color("#a7a7a7"))
	quitTextStyle     = lipgloss.NewStyle().Margin(1, 0, 2, 4)
)

type item struct {
	fmt.Stringer
}

func (i item) FilterValue() string { return "" }

type StringItem string

func (s StringItem) String() string { return string(s) }

type itemDelegate struct{}

func (d itemDelegate) Height() int                             { return 1 }
func (d itemDelegate) Spacing() int                            { return 0 }
func (d itemDelegate) Update(_ tea.Msg, _ *list.Model) tea.Cmd { return nil }
func (d itemDelegate) Render(w io.Writer, m list.Model, index int, listItem list.Item) {
	i, ok := listItem.(item)
	if !ok {
		return
	}

	str := i.String()

	var fn func(...string) string
	if index == m.Index() {
		fn = selectedItemStyle.Width(m.Width()).Render
	} else {
		fn = itemStyle.Width(m.Width()).Render
	}

	fmt.Fprint(w, fn(str))
}

// XXX: Generic?
type Model struct {
	width, height int
	list          list.Model
	quitting      bool
	err           error
}

func (m *Model) KeyMap() help.KeyMap {
	return m.list
}

// TODO: Use?
//
//	AdditionalShortHelpKeys func() []key.Binding
//	AdditionalFullHelpKeys  func() []key.Binding
func New(items []fmt.Stringer) *Model {
	var listItems []list.Item
	for _, i := range items {
		listItems = append(listItems, item{i})
	}

	l := list.New(listItems, itemDelegate{}, defaultWidth, listHeight)
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
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch keypress := msg.String(); keypress {
		case "enter":
			i, _ := m.list.SelectedItem().(item)
			cmds = append(cmds, util.MsgCmd(DropdownPickedMsg{i.Stringer}))
		case "esc":
			cmds = append(cmds, util.MsgCmd(DropdownExitMsg{}))
		}
	}

	util.UpdaterVal(&cmds, &m.list, msg)

	return m, tea.Batch(cmds...)
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
