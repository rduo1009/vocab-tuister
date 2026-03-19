package dropdown_test

import (
	"fmt"
	"io"
	"testing"
	"time"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/exp/teatest/v2"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/dropdown"
)

type model struct {
	Dropdown   *dropdown.Model
	CurrentMsg tea.Msg
}

func (m model) Init() tea.Cmd {
	return m.Dropdown.Init()
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg.(type) {
	case dropdown.PickedMsg, dropdown.ExitMsg:
		m.CurrentMsg = msg
		return m, tea.Quit
	}

	var cmd tea.Cmd

	m.Dropdown, cmd = m.Dropdown.Update(msg)

	return m, cmd
}

func (m model) View() tea.View {
	return tea.NewView(m.Dropdown.View())
}

const id = "testingDropdown"

type Option string

func (o Option) String() string {
	return string(o)
}

var optionStrings = []string{
	"Apple",
	"Banana",
	"Orange",
	"Pear",
	"Kiwi",
	"Peach",
	"Dragonfruit", // is the longest with 11 chars, so dropdown should have length 11+2=13
	"Pineapple",
	"Mangosteen",
	"Watermelon",
}

var (
	upKey    = tea.KeyPressMsg{Code: tea.KeyUp}
	downKey  = tea.KeyPressMsg{Code: tea.KeyDown}
	enterKey = tea.KeyPressMsg{Code: tea.KeyEnter}
)

func readBts(tb testing.TB, r io.Reader) []byte {
	tb.Helper()

	bts, err := io.ReadAll(r)
	if err != nil {
		tb.Fatal(err)
	}

	return bts
}

func TestDropdown(t *testing.T) {
	options := make([]fmt.Stringer, len(optionStrings))
	for i, v := range optionStrings {
		options[i] = Option(v)
	}

	dropdown := dropdown.New(id, options)
	m := model{Dropdown: dropdown}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	if err := tm.Quit(); err != nil {
		t.Fatal(err)
	}

	out := readBts(t, tm.FinalOutput(t, teatest.WithFinalTimeout(time.Second)))
	teatest.RequireEqualOutput(t, out)
}

func TestDropdownTyping(t *testing.T) {
	options := make([]fmt.Stringer, len(optionStrings))
	for i, v := range optionStrings {
		options[i] = Option(v)
	}

	d := dropdown.New(id, options)
	m := model{Dropdown: d}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	originalBts := readBts(t, tm.Output())

	tm.Type("lorem ipsum dolor sit amet")
	assert.Equal(
		t,
		originalBts,
		readBts(t, tm.Output()),
		"typing should not change anything",
	)
}

func TestDropdownCeiling(t *testing.T) {
	options := make([]fmt.Stringer, len(optionStrings))
	for i, v := range optionStrings {
		options[i] = Option(v)
	}

	d := dropdown.New(id, options)
	m := model{Dropdown: d}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	for range 12 {
		tm.Send(upKey)
	}

	tm.Send(enterKey)

	assert.Equal(t, dropdown.PickedMsg{ID: id, ChosenItem: options[0]}, tm.FinalModel(t).(model).CurrentMsg)
	assert.Equal(t, options[0].String(), m.Dropdown.LastSelected.String())
}

func TestDropdownFloor(t *testing.T) {
	options := make([]fmt.Stringer, len(optionStrings))
	for i, v := range optionStrings {
		options[i] = Option(v)
	}

	d := dropdown.New(id, options)
	m := model{Dropdown: d}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	for range 12 {
		tm.Send(downKey)
	}

	tm.Send(enterKey)

	assert.Equal(
		t,
		dropdown.PickedMsg{ID: id, ChosenItem: options[len(options)-1]},
		tm.FinalModel(t).(model).CurrentMsg,
	)
	assert.Equal(t, options[len(options)-1].String(), m.Dropdown.LastSelected.String())
}

func TestDropdownPickOption(t *testing.T) {
	options := make([]fmt.Stringer, len(optionStrings))
	for i, v := range optionStrings {
		options[i] = Option(v)
	}

	for i, o := range options {
		d := dropdown.New(id, options)
		m := model{Dropdown: d}
		tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))

		for range i {
			tm.Send(downKey)
		}

		tm.Send(enterKey)

		final := tm.FinalModel(t).(model)
		assert.Equal(t, dropdown.PickedMsg{ID: id, ChosenItem: o}, final.CurrentMsg)
		assert.Equal(t, o.String(), final.Dropdown.LastSelected.String())

		require.NoError(t, tm.Quit())
	}
}

func TestDropdownSetWidth(t *testing.T) {
	options := make([]fmt.Stringer, len(optionStrings))
	for i, v := range optionStrings {
		options[i] = Option(v)
	}
	d := dropdown.New(id, options)
	d.SetWidth(10)
	assert.Equal(t, 10, d.GetWidth())
}
