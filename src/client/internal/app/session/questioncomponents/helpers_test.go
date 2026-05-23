package questioncomponents

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
