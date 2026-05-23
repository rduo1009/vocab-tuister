package questioncomponents

import (
	"testing"

	"github.com/charmbracelet/x/exp/golden"

	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
)

func goldenSuffix(useNerdFonts bool) string {
	if useNerdFonts {
		return "_nerd"
	}
	return "_plain"
}

func newStyles(useNerdFonts bool) *styles.StylesWrapper {
	return &styles.StylesWrapper{
		Styles: styles.DefaultStyles(styles.DefaultThemes(true).Current(), false, useNerdFonts),
	}
}

func requireGoldenWithSuffix(t *testing.T, data []byte, useNerdFonts bool) {
	t.Helper()
	t.Run("fonts"+goldenSuffix(useNerdFonts), func(t *testing.T) {
		t.Helper()
		golden.RequireEqual(t, data)
	})
}
