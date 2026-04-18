package dropdown

import (
	"fmt"
	"io"

	"charm.land/bubbles/v2/help"
	"charm.land/bubbles/v2/key"
	"charm.land/bubbles/v2/list"
	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type (
	StartMsg  struct{ ID string }
	ExitMsg   struct{ ID string }
	PickedMsg struct {
		ID         string
		ChosenItem fmt.Stringer
	}
)

const defaultHeight = 5 // arbitrary

type item struct {
	fmt.Stringer
}

func (i item) FilterValue() string { return "" }

type itemDelegate struct {
	styles *styles.StylesWrapper
}

func (d itemDelegate) Height() int                             { return 1 }
func (d itemDelegate) Spacing() int                            { return 0 }
func (d itemDelegate) Update(_ tea.Msg, _ *list.Model) tea.Cmd { return nil }
func (d itemDelegate) Render(w io.Writer, m list.Model, index int, listItem list.Item) {
	i, ok := listItem.(item)
	if !ok {
		return
	}

	str := i.String()

	focused := index == m.Index()
	fmt.Fprint(w, d.styles.Dropdown.Item(focused).Width(m.Width()).Render(str))
}

// XXX: Generic?
type Model struct {
	ID            string
	LastSelected  fmt.Stringer
	width, height int
	list          list.Model
}

func (m *Model) KeyMap() help.KeyMap {
	return m.list
}

func New[T fmt.Stringer](id string, items []T, styles *styles.StylesWrapper) *Model {
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

	l := list.New(listItems, itemDelegate{styles: styles}, width, height)
	l.SetShowTitle(false)
	l.SetShowStatusBar(false)
	l.SetFilteringEnabled(false)
	l.SetShowPagination(false)
	l.SetShowHelp(false)
	l.DisableQuitKeybindings()
	l.InfiniteScrolling = true

	l.KeyMap.ShowFullHelp = key.NewBinding(
		key.WithKeys("ctrl+h"),
		key.WithHelp("ctrl+h", "toggle additional help"),
	)
	l.KeyMap.CloseFullHelp = key.NewBinding(
		key.WithKeys("ctrl+h"),
		key.WithHelp("ctrl+h", "toggle additional help"),
	)
	l.AdditionalShortHelpKeys = func() []key.Binding {
		return []key.Binding{
			key.NewBinding(
				key.WithKeys("enter"),
				key.WithHelp("enter", "submit"),
			),
			key.NewBinding(
				key.WithKeys("esc"),
				key.WithHelp("esc", "cancel"),
			),
			key.NewBinding(
				key.WithKeys("ctrl+q", "ctrl+c"),
				key.WithHelp("ctrl+q", "quit"),
			),
		}
	}
	l.AdditionalFullHelpKeys = func() []key.Binding {
		return []key.Binding{
			key.NewBinding(
				key.WithKeys("enter"),
				key.WithHelp("enter", "submit"),
			),
			key.NewBinding(
				key.WithKeys("esc"),
				key.WithHelp("esc", "cancel"),
			),
			key.NewBinding(
				key.WithKeys("ctrl+q", "ctrl+c"),
				key.WithHelp("ctrl+q", "quit"),
			),
		}
	}

	m := &Model{ID: id, LastSelected: items[0], list: l, width: width}
	m.width = width
	m.height = height

	return m
}

func (m *Model) Init() tea.Cmd {
	return nil
}

func (m *Model) Update(msg tea.Msg) (*Model, tea.Cmd) {
	if msg, ok := msg.(tea.KeyPressMsg); ok {
		switch keypress := msg.String(); keypress {
		case "enter":
			i, _ := m.list.SelectedItem().(item)
			m.LastSelected = i
			return m, util.MsgCmd(PickedMsg{ID: m.ID, ChosenItem: i.Stringer})

		case "esc":
			return m, util.MsgCmd(ExitMsg{ID: m.ID})
		}
	}

	var cmd tea.Cmd

	m.list, cmd = m.list.Update(msg)

	return m, cmd
}

func (m *Model) SetWidth(width int) {
	m.width = width
}

func (m *Model) GetWidth() int {
	return m.width
}

func (m *Model) SetHeight(height int) {
	m.height = height
}

func (m *Model) View() string {
	m.list.SetWidth(m.width)
	m.list.SetHeight(m.height)

	return m.list.View()
}
