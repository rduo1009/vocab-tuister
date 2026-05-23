package errordialog_test

import (
	"errors"
	"fmt"
	"os"
	"strings"
	"testing"
	"time"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/exp/golden"
	"github.com/stretchr/testify/assert"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/errordialog"
	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
)

const testWordWrapDialogWidth = 60

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

// TestErrorDialog checks the initial rendered output of the error dialog against a
// golden file.  Run with -update to regenerate the golden file.
func TestErrorDialog(t *testing.T) {
	ed := errordialog.New(newStyles())
	ed.SetWidth(100)
	ed.SetHeight(40)
	ed.SetError(errors.New("this is a test error"))
	requireGoldenWithSuffix(t, []byte(ed.View()))
}

// TestErrorDialogWordWrap checks long error text wraps to the viewport width.
// Run with -update to regenerate the golden file.
func TestErrorDialogWordWrap(t *testing.T) {
	ed := errordialog.New(newStyles())
	ed.SetWidth(testWordWrapDialogWidth)
	ed.SetHeight(40)
	ed.SetError(
		errors.New(
			"this is a very long error message that should wrap naturally and never require horizontal scrolling",
		),
	)
	requireGoldenWithSuffix(t, []byte(ed.View()))
}

func TestErrorDialogVisibility(t *testing.T) {
	ed := errordialog.New(newStyles())
	assert.False(t, ed.Visible())
	assert.Empty(t, ed.View())
	ed.SetError(errors.New("test error"))
	assert.True(t, ed.Visible())
	assert.NotEmpty(t, ed.View())
}

func TestErrorDialogInit(t *testing.T) {
	ed := errordialog.New(newStyles())
	assert.Nil(t, ed.Init())
}

func TestErrorDialogTimeoutInteraction(t *testing.T) {
	ed := errordialog.New(newStyles())
	ed.SetError(errors.New("test error"))
	assert.True(t, ed.Visible())
	ed, cmd := ed.Update(errordialog.TimeoutMsg{})
	assert.True(t, ed.Visible())
	assert.NotNil(t, cmd, "should return a new tick command")
}

func TestErrorDialogTimeoutHide(t *testing.T) {
	if testing.Short() {
		t.Skip("skipping slow test in short mode.")
	}

	t.Parallel()

	ed := errordialog.New(newStyles())
	ed.SetError(errors.New("test error"))
	time.Sleep(3100 * time.Millisecond)

	ed, cmd := ed.Update(errordialog.TimeoutMsg{})
	assert.False(t, ed.Visible())
	assert.Nil(t, cmd)
	assert.Empty(t, ed.View())
}

func TestErrorDialogScrolling(t *testing.T) {
	ed := errordialog.New(newStyles())
	ed.SetWidth(40 * 4)
	ed.SetHeight(20 * 4)

	var sb strings.Builder
	for i := range 30 {
		fmt.Fprintf(&sb, "error line %d\n", i)
	}

	sb.WriteString("error line 30")

	go ed.SetError(errors.New(sb.String()))

	time.Sleep(time.Millisecond * 100)

	assert.True(t, ed.Visible())
	initialView := ed.View()
	assert.Contains(t, initialView, "error line 0")
	assert.NotContains(t, initialView, "error line 30")

	for range 30 {
		ed, _ = ed.Update(tea.KeyPressMsg{Code: tea.KeyDown})
	}

	scrolledView := ed.View()
	assert.NotContains(t, scrolledView, "error line 0")
	assert.Contains(t, scrolledView, "error line 30")

	ed, _ = ed.Update(tea.MouseWheelMsg{Button: tea.MouseWheelUp})
	assert.NotEmpty(t, ed.View())
}

func TestErrorDialogResize(t *testing.T) {
	ed := errordialog.New(newStyles())
	ed.SetWidth(100)
	ed.SetHeight(100)
	ed.SetError(errors.New("error"))
	viewA := ed.View()

	ed.SetWidth(50)
	ed.SetHeight(50)
	viewB := ed.View()

	assert.NotEqual(t, viewA, viewB)
}
