package styles

import (
	"image/color"
	"math"

	"charm.land/lipgloss/v2"
	tint "github.com/lrstanley/bubbletint/v2"
	"github.com/lucasb-eyer/go-colorful"
)

func blend(cA, cB color.Color, t float64) color.Color {
	r1, g1, b1, a1 := cA.RGBA()
	r2, g2, b2, a2 := cB.RGBA()

	c1, _ := colorful.MakeColor(color.RGBA{
		R: uint8(r1 >> 8),
		G: uint8(g1 >> 8),
		B: uint8(b1 >> 8),
		A: uint8(a1 >> 8),
	})
	c2, _ := colorful.MakeColor(color.RGBA{
		R: uint8(r2 >> 8),
		G: uint8(g2 >> 8),
		B: uint8(b2 >> 8),
		A: uint8(a2 >> 8),
	})

	blended := c1.BlendLab(c2, t)
	r, g, b := blended.RGB255()

	return lipgloss.RGBColor{R: r, G: g, B: b}
}

func colorDistance(a, b color.Color) float64 {
	ar, ag, ab, _ := a.RGBA()
	br, bg, bb, _ := b.RGBA()
	dr := float64(ar) - float64(br)
	dg := float64(ag) - float64(bg)
	db := float64(ab) - float64(bb)
	return math.Sqrt(dr*dr + dg*dg + db*db)
}

// Colours contains basic colours used by the vocab-tuister styles.
type Colours struct {
	// Default colours

	Fg     color.Color
	Bg     color.Color
	Black  color.Color
	Blue   color.Color
	Cyan   color.Color
	Green  color.Color
	Red    color.Color
	White  color.Color
	Yellow color.Color

	// Custom colours

	Pink   color.Color
	Purple color.Color
	Coral  color.Color
	Orange color.Color
}

// pinkPurple returns pink and purple [color.Color] based on the theme provided.
//
// Some bubbletint themes do not have a truly purple colour in [tint.Tint.Purple]. Rather, often the colour is pink.
// The styles need to have these as separate colours, so a 'true pink' and 'true purple' need to be determined.
func pinkPurple(theme *tint.Tint) (pink, purple color.Color) {
	testPurple := blend(theme.Red, theme.Blue, 0.7)
	testPink := lipgloss.Lighten(theme.Red, 0.3)

	themePurple := theme.Purple // bubbletint's potentially-pink "purple"
	distToPurple := colorDistance(themePurple, testPurple)
	distToPink := colorDistance(themePurple, testPink)

	if distToPink < distToPurple {
		// theme.Purple is actually closer to pink — use it as pink
		pink = themePurple
		purple = testPurple
	} else {
		// theme.Purple is genuinely purple — use it as purple
		purple = themePurple
		pink = testPink
	}
	return pink, purple
}

func DefaultColours(theme *tint.Tint) *Colours {
	// TODO: tweak percentages
	pink, purple := pinkPurple(theme)
	orange := blend(theme.Red, theme.Yellow, 0.5)
	coral := blend(theme.Red, orange, 0.5)

	return &Colours{
		Fg:     theme.Fg,
		Bg:     theme.Bg,
		Black:  theme.Black,
		Blue:   theme.Blue,
		Cyan:   theme.Cyan,
		Green:  theme.Green,
		Red:    theme.Red,
		White:  theme.White,
		Yellow: theme.Yellow,

		Pink:   pink,
		Purple: purple,
		Coral:  coral,
		Orange: orange,
	}
}
