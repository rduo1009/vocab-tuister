package styles

import (
	"fmt"
	"image/color"
	"math"
	"strings"

	"charm.land/bubbles/v2/filepicker"
	"charm.land/fang/v2"
	"charm.land/huh/v2"
	"charm.land/lipgloss/v2"
	"github.com/alecthomas/chroma/v2"
	"github.com/ionut-t/goeditor"
	"github.com/lrstanley/bubbletint/chromatint/v2"
	tint "github.com/lrstanley/bubbletint/v2"
	"github.com/lucasb-eyer/go-colorful"
)

type StylesWrapper struct{ Styles }

type Styles struct {
	Title  lipgloss.Style
	Bold   lipgloss.Style
	Italic lipgloss.Style
	Faint  lipgloss.Style
	Error  lipgloss.Style // red text without bolding or italics

	TabBorder     func(active, focused bool, pad int) lipgloss.Style
	TabGap        func(focused bool) lipgloss.Style
	NormalBorder  func(focused bool) lipgloss.Style
	OverlayBorder lipgloss.Style
	Button        func(active, focused bool) lipgloss.Style
	Scrollbar     func(height, total, visible, offset int) string

	LoadSection struct {
		LabelMissing lipgloss.Style
		LabelPending lipgloss.Style
		LabelLoaded  lipgloss.Style
		LabelSep     lipgloss.Style
	}

	SessionPage struct {
		Correct   lipgloss.Style
		Incorrect lipgloss.Style
	}

	MultipleChoice struct {
		Option     func(focused bool, color color.Color) lipgloss.Style
		Unanswered color.Color
		Correct    color.Color
		Incorrect  color.Color
	}

	Dropdown struct {
		Item func(focused bool) lipgloss.Style
	}

	ErrorDialog struct {
		Border lipgloss.Style
		Header lipgloss.Style
	}

	Filepicker filepicker.Styles

	Editor struct {
		goeditor.Theme
		Chroma *chroma.Style
	}

	Form huh.Theme

	Jsonview *chroma.Style

	Fang fang.ColorSchemeFunc
}

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

func hexColor(c color.Color) string {
	rgba := color.RGBAModel.Convert(c).(color.RGBA)
	return fmt.Sprintf("#%.2x%.2x%.2x", rgba.R, rgba.G, rgba.B)
}

func DefaultStyles(theme *tint.Tint) Styles {
	// TODO: Refactor these out into colors.go
	// and then tweak the percentages a little
	truePurple := blend(theme.Red, theme.Blue, 0.7)
	trueOrange := blend(theme.Red, theme.Yellow, 0.5)
	trueCoral := blend(theme.Red, trueOrange, 0.5)

	s := Styles{}

	s.Title = lipgloss.NewStyle().Bold(true).Underline(true)
	s.Bold = lipgloss.NewStyle().Bold(true)
	s.Italic = lipgloss.NewStyle().Italic(true)
	s.Faint = lipgloss.NewStyle().Faint(true)
	s.Error = lipgloss.NewStyle().Foreground(theme.Red)

	inactiveTabBorder := func() lipgloss.Border {
		b := lipgloss.RoundedBorder()
		b.BottomLeft = "┴"
		b.BottomRight = "┴"
		return b
	}()
	activeTabBorder := func() lipgloss.Border {
		b := lipgloss.RoundedBorder()
		b.Bottom = " "
		b.BottomLeft = "┘"
		b.BottomRight = "└"
		return b
	}()
	s.TabBorder = func(active, focused bool, pad int) lipgloss.Style {
		var style lipgloss.Style
		if active {
			style = style.Border(activeTabBorder, true)
		} else {
			style = style.Border(inactiveTabBorder, true)
		}

		if focused {
			style = style.BorderForeground(theme.Blue)
		} else {
			style = style.BorderForeground(theme.White)
		}

		return style.Padding(0, pad)
	}
	s.TabGap = func(focused bool) lipgloss.Style {
		style := lipgloss.NewStyle().Border(inactiveTabBorder, true)
		if focused {
			style = style.BorderForeground(theme.Blue)
		} else {
			style = style.BorderForeground(theme.White)
		}

		return style.BorderTop(false).
			BorderLeft(false).
			BorderRight(false)
	}

	s.NormalBorder = func(focused bool) lipgloss.Style {
		if focused {
			return lipgloss.NewStyle().Border(lipgloss.RoundedBorder()).BorderForeground(theme.Blue)
		}
		return lipgloss.NewStyle().Border(lipgloss.RoundedBorder()).BorderForeground(theme.White)
	}
	s.OverlayBorder = lipgloss.NewStyle().Border(lipgloss.RoundedBorder()).BorderForeground(theme.Cyan)

	s.Button = func(active, focused bool) lipgloss.Style {
		style := lipgloss.NewStyle().Padding(0, 1)

		if active {
			style = style.Foreground(lipgloss.Color("#fff7db")).
				Background(lipgloss.Color("#888b7e"))
		} else {
			style = style.Foreground(lipgloss.Color("#a9a9a9")).
				Background(lipgloss.Color("#555555"))
		}

		if focused {
			style = style.Italic(true).Underline(true)
		}

		return style
	}

	s.Scrollbar = func(height, total, visible, offset int) string {
		if height == 0 {
			return ""
		}

		if total <= visible {
			return strings.TrimRight(strings.Repeat(" \n", height), "\n")
		}

		ratio := float64(height) / float64(total)
		thumbHeight := int(math.Max(1, math.Round(float64(visible)*ratio)))
		// Bounds check
		thumbOffset := max(0, min(int(math.Round(float64(offset)*ratio)), height-thumbHeight))

		trackStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("#585858"))
		thumbStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("#bcbcbc"))

		trackChar := "│"
		thumbChar := "█"

		track := trackStyle.Render(trackChar)
		thumb := thumbStyle.Render(thumbChar)

		bar := ""

		var barSb185 strings.Builder
		for i := range height {
			if i >= thumbOffset && i < thumbOffset+thumbHeight {
				barSb185.WriteString(thumb + "\n")
			} else {
				barSb185.WriteString(track + "\n")
			}
		}

		bar += barSb185.String()

		return strings.TrimRight(bar, "\n")
	}

	s.LoadSection.LabelMissing = lipgloss.NewStyle().Foreground(theme.Red)
	s.LoadSection.LabelPending = lipgloss.NewStyle().Foreground(theme.Yellow)
	s.LoadSection.LabelLoaded = lipgloss.NewStyle().Foreground(theme.Green)
	s.LoadSection.LabelSep = lipgloss.NewStyle().Foreground(lipgloss.Lighten(theme.Black, 0.1))

	s.SessionPage.Correct = lipgloss.NewStyle().Bold(true).Foreground(theme.Green)
	s.SessionPage.Incorrect = lipgloss.NewStyle().Bold(true).Foreground(theme.Red)

	s.MultipleChoice.Option = func(focused bool, color color.Color) lipgloss.Style {
		borderColor := color
		if focused {
			if color == theme.White {
				borderColor = theme.Purple
			} else {
				borderColor = lipgloss.Lighten(borderColor, 0.1)
			}
		}

		return lipgloss.NewStyle().
			Padding(0, 4).
			MarginBottom(1).
			Border(lipgloss.NormalBorder()).
			BorderForeground(borderColor).
			Align(lipgloss.Left)
	}
	s.MultipleChoice.Unanswered = theme.White
	s.MultipleChoice.Correct = theme.Green
	s.MultipleChoice.Incorrect = theme.Red

	s.Dropdown.Item = func(selected bool) lipgloss.Style {
		if selected {
			return lipgloss.NewStyle().Background(lipgloss.Color("#a7a7a7")).Padding(0, 1)
		}
		return lipgloss.NewStyle().Background(lipgloss.Color("#707070")).Padding(0, 1)
	}

	s.ErrorDialog.Border = lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(theme.Red)
	s.ErrorDialog.Header = lipgloss.NewStyle().
		Foreground(theme.Red).
		Bold(true).
		Padding(0, 1).
		Border(lipgloss.NormalBorder(), false, false, true, false).
		BorderForeground(theme.Red)

	s.Filepicker = filepicker.DefaultStyles()
	s.Filepicker.Cursor = lipgloss.NewStyle().Foreground(theme.Purple)
	s.Filepicker.Symlink = lipgloss.NewStyle().Foreground(theme.Green)
	s.Filepicker.Directory = lipgloss.NewStyle().Foreground(truePurple)
	s.Filepicker.EmptyDirectory = s.Filepicker.EmptyDirectory.SetString("No files found.")
	s.Filepicker.Selected = s.Filepicker.Selected.Foreground(theme.Purple)

	s.Editor.Theme = goeditor.DefaultTheme(theme.Dark)
	s.Editor.NormalModeStyle = s.Editor.NormalModeStyle.Background(theme.Cyan)
	s.Editor.InsertModeStyle = s.Editor.InsertModeStyle.Background(theme.Blue)
	styleEntryVocab := chromatint.StyleEntry(theme, false)
	styleEntryVocab[chroma.GenericHeading] = fmt.Sprintf("bold %s", hexColor(trueOrange))
	styleEntryVocab[chroma.GenericStrong] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: theme.Fg, Bold: true},
		theme.Dark,
	)
	styleEntryVocab[chroma.Comment] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: lipgloss.Lighten(theme.Bg, 0.3), Italic: true},
		theme.Dark,
	)
	styleEntryVocab[chroma.CommentPreproc] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: lipgloss.Lighten(theme.Bg, 0.3)},
		theme.Dark,
	)
	s.Editor.Chroma = chroma.MustNewStyle("bubbletint_vocabeditor", styleEntryVocab)

	s.Form = huh.ThemeFunc(func(isDark bool) *huh.Styles {
		formStyles := huh.ThemeCharm(theme.Dark)
		formStyles.Focused.Title = formStyles.Focused.Title.Foreground(truePurple)
		formStyles.Focused.NoteTitle = formStyles.Focused.NoteTitle.Foreground(truePurple)
		formStyles.Focused.Directory = formStyles.Focused.Directory.Foreground(truePurple)
		formStyles.Focused.ErrorIndicator = formStyles.Focused.ErrorIndicator.Foreground(theme.Red)
		formStyles.Focused.ErrorMessage = formStyles.Focused.ErrorMessage.Foreground(theme.Red)
		formStyles.Focused.SelectSelector = formStyles.Focused.SelectSelector.Foreground(theme.Purple)
		formStyles.Focused.NextIndicator = formStyles.Focused.NextIndicator.Foreground(theme.Purple)
		formStyles.Focused.PrevIndicator = formStyles.Focused.PrevIndicator.Foreground(theme.Purple)
		formStyles.Focused.MultiSelectSelector = formStyles.Focused.MultiSelectSelector.Foreground(theme.Purple)
		formStyles.Focused.SelectedOption = formStyles.Focused.SelectedOption.Foreground(theme.Green)
		formStyles.Focused.SelectedPrefix = formStyles.Focused.SelectedPrefix.Foreground(theme.Green)
		formStyles.Focused.UnselectedOption = formStyles.Focused.UnselectedOption.Foreground(theme.Fg)
		formStyles.Focused.FocusedButton = formStyles.Focused.FocusedButton.Foreground(theme.Bg).
			Background(theme.Purple)
		formStyles.Focused.BlurredButton = formStyles.Focused.BlurredButton.Foreground(theme.Fg).
			Background(theme.Bg)

		formStyles.Focused.TextInput.Cursor = formStyles.Focused.TextInput.Cursor.Foreground(
			lipgloss.Color("#f2d5cf"),
		)
		formStyles.Focused.TextInput.Placeholder = formStyles.Focused.TextInput.Placeholder.Foreground(
			lipgloss.Lighten(theme.Bg, 0.2),
		)
		formStyles.Focused.TextInput.Prompt = formStyles.Focused.TextInput.Prompt.Foreground(theme.Purple)

		formStyles.Blurred = formStyles.Focused
		formStyles.Blurred.Base = formStyles.Blurred.Base.BorderStyle(lipgloss.HiddenBorder())
		formStyles.Blurred.Card = formStyles.Blurred.Base

		formStyles.Group.Title = formStyles.Focused.Title
		formStyles.Group.Description = formStyles.Focused.Description

		return formStyles
	})

	styleEntryJSON := chromatint.StyleEntry(theme, false)
	styleEntryJSON[chroma.NameTag] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: truePurple},
		theme.Dark,
	)
	styleEntryJSON[chroma.LiteralNumber] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: trueOrange},
		theme.Dark,
	)
	s.Jsonview = chroma.MustNewStyle("bubbletint_json", styleEntryJSON)

	s.Fang = func(lightDark lipgloss.LightDarkFunc) fang.ColorScheme {
		// NOTE: Using closest equivalents in the theme for the charmtone colours
		cs := fang.DefaultColorScheme(lightDark)
		cs.Title = truePurple                                // ct.Charple
		cs.Program = theme.Blue                              // ld(ct.Malibu, ct.Guppy) (fsr these colours are completely different, using Malibu)
		cs.Command = theme.Purple                            // ld(ct.Pony, ct.Cheeky)
		cs.Flag = theme.Green                                // ld(lipgloss.Color("#0CB37F"), ct.Guac)
		cs.QuotedString = trueCoral                          // ld(ct.Coral, charmtone.Salmon)
		cs.ErrorHeader = [2]color.Color{theme.Bg, theme.Red} // ct.Butter, ct.Cherry
		return cs
	}

	return s
}
