package tabs

import (
	"os"
	"testing"

	"github.com/charmbracelet/x/exp/golden"

	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
)

var useNerdFonts bool

func TestMain(m *testing.M) {
	// First run with nerd fonts disabled
	useNerdFonts = false
	code := m.Run()
	if code != 0 {
		os.Exit(code)
	}

	// Second run with nerd fonts enabled
	useNerdFonts = true
	code = m.Run()
	os.Exit(code)
}

func goldenSuffix() string {
	if useNerdFonts {
		return "_nerd"
	}
	return "_plain"
}

func newStyles() *styles.StylesWrapper {
	return &styles.StylesWrapper{
		Styles: styles.DefaultStyles(styles.DefaultThemes(true).Current(), false, useNerdFonts),
	}
}

func requireGoldenWithSuffix(t *testing.T, data []byte) {
	t.Helper()
	t.Run("fonts"+goldenSuffix(), func(t *testing.T) {
		t.Helper()
		golden.RequireEqual(t, data)
	})
}

type tabName string

func (s tabName) DisplayString(*styles.StylesWrapper) string { return string(s) }

func TestView(t *testing.T) {
	names := []TabName{
		tabName("Tab 1"),
		tabName("Tab 2"),
		tabName("Tab 3"),
	}

	testCases := []struct {
		name      string
		active    int
		isFocused bool
		width     int
	}{
		{name: "first_tab_active_blurred", active: 0, isFocused: false, width: 40},
		{name: "second_tab_active_focused", active: 1, isFocused: true, width: 40},
		{name: "third_tab_active_blurred", active: 2, isFocused: false, width: 40},
		{name: "narrow_width", active: 0, isFocused: true, width: 20},
		{name: "wide_width", active: 1, isFocused: false, width: 80},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			m := New(names, tc.active, tc.isFocused, newStyles())
			m.Width = tc.width
			requireGoldenWithSuffix(t, []byte(m.View()))
		})
	}
}

func TestModelSelection(t *testing.T) {
	names := []TabName{
		tabName("Tab 1"),
		tabName("Tab 2"),
		tabName("Tab 3"),
	}
	m := New(names, 0, false, newStyles())

	if m.active != 0 {
		t.Errorf("expected active tab 0, got %d", m.active)
	}

	m.Next()

	if m.active != 1 {
		t.Errorf("expected active tab 1 after Next(), got %d", m.active)
	}

	m.Prev()

	if m.active != 0 {
		t.Errorf("expected active tab 0 after Prev(), got %d", m.active)
	}

	m.Select(2)

	if m.active != 2 {
		t.Errorf("expected active tab 2 after Select(2), got %d", m.active)
	}
}

func TestFocusBlur(t *testing.T) {
	names := []TabName{tabName("Tab 1")}
	m := New(names, 0, false, newStyles())

	if m.Focused() {
		t.Error("expected initial focus to be false")
	}

	m.Focus()

	if !m.Focused() {
		t.Error("expected focused to be true after Focus()")
	}

	m.Blur()

	if m.Focused() {
		t.Error("expected focused to be false after Blur()")
	}
}
