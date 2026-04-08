package jsonview_test

import (
	"fmt"
	"io"
	"strings"
	"testing"
	"time"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/exp/teatest/v2"
	"github.com/stretchr/testify/assert"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/jsonview"
)

type model struct {
	JSONView *jsonview.Model
}

func (m model) Init() tea.Cmd {
	return m.JSONView.Init()
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd
	var newView any
	newView, cmd = m.JSONView.Update(msg)
	m.JSONView = newView.(*jsonview.Model)

	return m, cmd
}

func (m model) View() tea.View {
	return tea.NewView(m.JSONView.View())
}

func readBts(tb testing.TB, r io.Reader) []byte {
	tb.Helper()

	bts, err := io.ReadAll(r)
	if err != nil {
		tb.Fatal(err)
	}

	return bts
}

func TestJSONView(t *testing.T) {
	jb := `{"foo":"bar"}`
	jv := jsonview.New(jb)
	jv.SetWidth(20)
	jv.SetHeight(10)

	m := model{JSONView: jv}
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

func TestJSONViewScrolling(t *testing.T) {
	// Create a long JSON string (25 lines)
	var sb strings.Builder
	sb.WriteString("[\n")
	for i := 0; i < 25; i++ {
		sb.WriteString(fmt.Sprintf("  {\"id\": %d, \"data\": \"item %d\"}", i, i))
		if i < 24 {
			sb.WriteString(",")
		}
		sb.WriteString("\n")
	}
	sb.WriteString("]")
	jb := sb.String()

	jv := jsonview.New(jb)
	jv.SetWidth(60)
	jv.SetHeight(10) // Small height to ensure scrolling is needed

	m := model{JSONView: jv}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	// Initial check: top items visible, bottom items NOT visible
	initialView := jv.View()
	assert.Contains(t, initialView, "item 0")
	assert.Contains(t, initialView, "item 1")
	assert.NotContains(t, initialView, "item 20")

	// Scroll down multiple times
	for i := 0; i < 30; i++ {
		tm.Send(tea.KeyPressMsg{Code: tea.KeyDown})
	}

	if err := tm.Quit(); err != nil {
		t.Fatal(err)
	}

	finalModel := tm.FinalModel(t).(model)
	scrolledView := finalModel.JSONView.View()

	// After scrolling down: bottom items visible, top items NOT visible
	assert.Contains(t, scrolledView, "item 20")
	assert.Contains(t, scrolledView, "item 24")
	assert.NotContains(t, scrolledView, "item 0")

	// Now let's test scrolling back up in a new model to be clean or continue
	jv2 := jsonview.New(jb)
	jv2.SetWidth(60)
	jv2.SetHeight(10)
	m2 := model{JSONView: jv2}
	tm2 := teatest.NewTestModel(t, m2, teatest.WithInitialTermSize(70, 30))

	// Scroll down
	for i := 0; i < 30; i++ {
		tm2.Send(tea.KeyPressMsg{Code: tea.KeyDown})
	}
	// Scroll back up
	for i := 0; i < 30; i++ {
		tm2.Send(tea.KeyPressMsg{Code: tea.KeyUp})
	}

	if err := tm2.Quit(); err != nil {
		t.Fatal(err)
	}

	upView := tm2.FinalModel(t).(model).JSONView.View()
	assert.Contains(t, upView, "item 0")
	assert.NotContains(t, upView, "item 20")
}

func TestJSONViewHorizontalScrolling(t *testing.T) {
	// Single long line that will definitely exceed width 20
	jb := `{"very_long_key_name_that_should_require_horizontal_scrolling": "some_value_that_is_also_very_long"}`
	jv := jsonview.New(jb)
	jv.SetWidth(20)
	jv.SetHeight(5)

	m := model{JSONView: jv}
	tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(70, 30))
	t.Cleanup(func() {
		if err := tm.Quit(); err != nil {
			t.Fatal(err)
		}
	})

	// Initial check: start of the line visible
	initialView := jv.View()
	assert.Contains(t, initialView, "very_long_key")
	// The end of the line should NOT be visible initially
	assert.NotContains(t, initialView, "also_very_long")

	// Scroll right
	for i := 0; i < 50; i++ {
		tm.Send(tea.KeyPressMsg{Code: tea.KeyRight})
	}

	if err := tm.Quit(); err != nil {
		t.Fatal(err)
	}

	scrolledView := tm.FinalModel(t).(model).JSONView.View()
	// After scrolling right: the end should be visible
	assert.Contains(t, scrolledView, "also_very_long")
	// And the start should NOT be visible (or at least less of it)
	assert.NotContains(t, scrolledView, "{\"very_long")

	// Now test scrolling back left
	jv2 := jsonview.New(jb)
	jv2.SetWidth(20)
	jv2.SetHeight(5)
	m2 := model{JSONView: jv2}
	tm2 := teatest.NewTestModel(t, m2, teatest.WithInitialTermSize(70, 30))

	// Scroll right then back left
	for i := 0; i < 50; i++ {
		tm2.Send(tea.KeyPressMsg{Code: tea.KeyRight})
	}
	for i := 0; i < 50; i++ {
		tm2.Send(tea.KeyPressMsg{Code: tea.KeyLeft})
	}

	if err := tm2.Quit(); err != nil {
		t.Fatal(err)
	}

	leftView := tm2.FinalModel(t).(model).JSONView.View()
	assert.Contains(t, leftView, "very_long_key")
	assert.NotContains(t, leftView, "also_very_long")
}

func TestJSONViewSetContent(t *testing.T) {
	jb1 := `{"foo":"bar"}`
	jb2 := `{"baz":"qux"}`
	jv := jsonview.New(jb1)
	jv.SetWidth(20)
	jv.SetHeight(10)

	jv.SetContent(jb2)

	// Since highlighting might wrap words with ANSI codes, we use strings.Contains
	// We check for the raw content values
	view := jv.View()
	assert.Contains(t, view, "baz")
	assert.Contains(t, view, "qux")
	assert.NotContains(t, view, "foo")
}

func TestJSONViewDimensions(t *testing.T) {
	jb := `{"foo":"bar"}`
	jv := jsonview.New(jb)

	jv.SetWidth(50)
	jv.SetHeight(20)

	// View should at least return some content
	assert.NotEmpty(t, jv.View())
}

func TestJSONViewKeyMap(t *testing.T) {
	jb := `{"foo":"bar"}`
	jv := jsonview.New(jb)

	km := jv.KeyMap()
	assert.NotNil(t, km)
	assert.NotEmpty(t, km.ShortHelp())
	assert.NotEmpty(t, km.FullHelp())
}
