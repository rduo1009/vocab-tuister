package questioncomponents

import (
	"os"
	"testing"

	"github.com/charmbracelet/x/exp/golden"

	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
)

func nerdFontsEnabled() bool {
	return os.Getenv("NERD_FONTS") == "1"
}

func goldenSuffix() string {
	if nerdFontsEnabled() {
		return "_nerd"
	}
	return "_plain"
}

func newStyles() *styles.StylesWrapper {
	nerd := nerdFontsEnabled()
	return &styles.StylesWrapper{
		Styles: styles.DefaultStyles(styles.DefaultThemes(nerd).Current(), nerd),
	}
}

func requireGoldenWithSuffix(t *testing.T, data []byte) {
	t.Helper()
	t.Run("fonts"+goldenSuffix(), func(t *testing.T) {
		t.Helper()
		golden.RequireEqual(t, data)
	})
}
