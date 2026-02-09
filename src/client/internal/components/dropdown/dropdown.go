package dropdown

import (
	"fmt"
	"io"

	"charm.land/bubbles/v2/help"
	"charm.land/bubbles/v2/list"
	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type (
	StartMsg  struct{}
	ExitMsg   struct{}
	PickedMsg struct{ ChosenItem fmt.Stringer }
)

const defaultHeight = 5 // arbitrary

var (
	itemStyle         = lipgloss.NewStyle().Background(lipgloss.Color("#707070")).Padding(0, 1)
	selectedItemStyle = lipgloss.NewStyle().Background(lipgloss.Color("#a7a7a7")).Padding(0, 1)
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
	var (
		listItems []list.Item
		maxWidth  int
	)

	for _, i := range items {
		s := i.String()

		w := lipgloss.Width(s)
		if w > maxWidth {
			maxWidth = w
		}

		listItems = append(listItems, item{i})
	}

	width := maxWidth + 2

	height := min(len(items), defaultHeight)
	if height == 0 {
		height = 1
	}

	l := list.New(listItems, itemDelegate{}, width, height)
	l.SetShowTitle(false)
	l.SetShowStatusBar(false)
	l.SetFilteringEnabled(false)
	l.SetShowPagination(false)
	l.SetShowHelp(false)

	m := &Model{list: l}
	m.width = width
	m.height = height

	return m
}

func (m *Model) Init() tea.Cmd {
	return nil
}

func (m *Model) Update(msg tea.Msg) (app.ComponentModel, tea.Cmd) {
	var cmds []tea.Cmd

	if msg, ok := msg.(tea.KeyMsg); ok {
		switch keypress := msg.String(); keypress {
		case "enter":
			i, _ := m.list.SelectedItem().(item)
			cmds = append(cmds, util.MsgCmd(PickedMsg{i.Stringer}))

		case "esc": // FIXME: fsr this quits the whole app???
			cmds = append(cmds, util.MsgCmd(ExitMsg{}))
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

	return m.list.View()
}
