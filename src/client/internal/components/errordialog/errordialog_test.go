package errordialog_test

import (
	"errors"
	"fmt"
	"testing"
	"time"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/exp/golden"
	"github.com/stretchr/testify/assert"

	"github.com/rduo1009/vocab-tuister/src/client/internal/components/errordialog"
	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
)

// TestErrorDialog checks the initial rendered output of the error dialog against a
// golden file.  Run with -update to regenerate the golden file.
func TestErrorDialog(t *testing.T) {
	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	ed := errordialog.New(&s)
	ed.SetWidth(100)
	ed.SetHeight(40)
	ed.SetError(errors.New("this is a test error"))

	finalView := ed.View()
	golden.RequireEqual(t, []byte(finalView))
}

func TestErrorDialogVisibility(t *testing.T) {
	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	ed := errordialog.New(&s)
	assert.False(t, ed.Visible())
	assert.Empty(t, ed.View()) // Should return empty string when invisible

	ed.SetError(errors.New("test error"))
	assert.True(t, ed.Visible())
	assert.NotEmpty(t, ed.View())
}

func TestErrorDialogInit(t *testing.T) {
	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	ed := errordialog.New(&s)
	assert.Nil(t, ed.Init())
}

func TestErrorDialogTimeoutInteraction(t *testing.T) {
	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	ed := errordialog.New(&s)
	ed.SetError(errors.New("test error"))
	assert.True(t, ed.Visible())

	// Setting error updates the last interaction time.
	// Sending TimeoutMsg immediately should NOT hide the dialog,
	// because the recent interaction threshold (3s) hasn't passed.
	ed, cmd := ed.Update(errordialog.TimeoutMsg{})

	assert.True(t, ed.Visible())
	assert.NotNil(t, cmd, "should return a new tick command")
}

func TestErrorDialogTimeoutHide(t *testing.T) {
	if testing.Short() {
		t.Skip("skipping slow test in short mode.")
	}
	t.Parallel()

	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	ed := errordialog.New(&s)
	ed.SetError(errors.New("test error"))

	// Wait past the 3-second threshold to allow TimeoutMsg to hide it
	time.Sleep(3100 * time.Millisecond)

	ed, cmd := ed.Update(errordialog.TimeoutMsg{})

	assert.False(t, ed.Visible())
	assert.Nil(t, cmd)
	assert.Empty(t, ed.View())
}

func TestErrorDialogScrolling(t *testing.T) {
	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	ed := errordialog.New(&s)
	ed.SetWidth(40 * 4)
	ed.SetHeight(20 * 4) // Height gives around 20-5 = 15 viewport height

	var errStr string
	for i := 0; i < 30; i++ {
		errStr += fmt.Sprintf("error line %d\n", i)
	}
	errStr += "error line 30"
	go ed.SetError(errors.New(errStr))
	time.Sleep(time.Millisecond * 100)
	assert.True(t, ed.Visible())

	initialView := ed.View()
	assert.Contains(t, initialView, "error line 0")
	assert.NotContains(t, initialView, "error line 30")

	// Scroll down using key messages
	for i := 0; i < 30; i++ {
		ed, _ = ed.Update(tea.KeyPressMsg{Code: tea.KeyDown})
	}

	scrolledView := ed.View()
	assert.NotContains(t, scrolledView, "error line 0")
	assert.Contains(t, scrolledView, "error line 30")

	// Mouse scrolling interaction
	ed, _ = ed.Update(tea.MouseWheelMsg{Button: tea.MouseWheelUp})

	scrolledUpView := ed.View()
	assert.NotEmpty(t, scrolledUpView)
}

func TestErrorDialogResize(t *testing.T) {
	s := styles.StylesWrapper{Styles: styles.DefaultStyles(styles.DefaultThemes().Current())}
	ed := errordialog.New(&s)
	ed.SetWidth(100)
	ed.SetHeight(100)
	ed.SetError(errors.New("error"))

	viewA := ed.View()

	ed.SetWidth(50)
	ed.SetHeight(50)
	viewB := ed.View()

	assert.NotEqual(t, viewA, viewB)
}
