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

// nerdFontsEnabled returns true when the NERD_FONTS environment variable is set to "1".
func nerdFontsEnabled() bool {
	return os.Getenv("NERD_FONTS") == "1"
}

// goldenSuffix returns a filename suffix based on the current NERD_FONTS setting,
// so that each font mode gets its own golden file.
func goldenSuffix() string {
	if nerdFontsEnabled() {
		return "_nerd"
	}
	return "_plain"
}

// newStyles creates a StylesWrapper that respects the NERD_FONTS env variable.
func newStyles() *styles.StylesWrapper {
	nerd := nerdFontsEnabled()
	return &styles.StylesWrapper{
		Styles: styles.DefaultStyles(styles.DefaultThemes(true).Current(), nerd),
	}
}

// requireGoldenWithSuffix calls golden.RequireEqual against a file whose name
// is derived from the test name plus the nerd-fonts suffix.  Pass -update to
// regenerate all golden files at once.
func requireGoldenWithSuffix(t *testing.T, data []byte) {
	t.Helper()
	// golden.RequireEqual uses t.Name() internally, so we run a named subtest
	// whose name embeds the suffix — that way both sets of golden files can
	// live side-by-side without colliding.
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
