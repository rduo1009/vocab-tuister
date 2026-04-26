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
)

type StylesWrapper struct{ Styles }

type Styles struct {
	Text   lipgloss.Style
	Title  lipgloss.Style
	Bold   lipgloss.Style
	Italic lipgloss.Style
	Faint  lipgloss.Style
	Error  lipgloss.Style // red text without bolding or italics

	Overlay struct {
		Title  lipgloss.Style
		Bold   lipgloss.Style
		Italic lipgloss.Style
		Faint  lipgloss.Style
		Error  lipgloss.Style // red text without bolding or italics
	}

	TabBorder      func(active, focused bool, pad int) lipgloss.Style
	TabGap         func(focused bool) lipgloss.Style
	NormalBorder   func(focused bool) lipgloss.Style
	OverlayBorder  lipgloss.Style
	Button         func(active, focused bool) lipgloss.Style
	DropdownButton func(active, focused bool, label string, width, marginLeft int) string
	Scrollbar      func(height, total, visible, offset int) string

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

func hexColor(c color.Color) string {
	rgba := color.RGBAModel.Convert(c).(color.RGBA)
	return fmt.Sprintf("#%.2x%.2x%.2x", rgba.R, rgba.G, rgba.B)
}

func DefaultStyles(theme *tint.Tint, overlayActive bool) Styles {
	overlayDim := func(c color.Color) color.Color {
		if overlayActive {
			return lipgloss.Darken(c, 0.4)
		} else {
			return c
		}
	}

	colours := DefaultColours(theme)
	s := Styles{}

	s.Text = lipgloss.NewStyle().Foreground(overlayDim(colours.Fg))
	s.Title = lipgloss.NewStyle().Bold(true).Underline(true).Foreground(overlayDim(colours.Fg))
	s.Bold = lipgloss.NewStyle().Bold(true).Foreground(overlayDim(colours.Fg))
	s.Italic = lipgloss.NewStyle().Italic(true).Foreground(overlayDim(colours.Fg))
	s.Faint = lipgloss.NewStyle().Faint(true).Foreground(overlayDim(colours.Fg))
	s.Error = lipgloss.NewStyle().Foreground(overlayDim(colours.Red))

	s.Overlay.Title = lipgloss.NewStyle().Bold(true).Underline(true)
	s.Overlay.Bold = lipgloss.NewStyle().Bold(true)
	s.Overlay.Italic = lipgloss.NewStyle().Italic(true)
	s.Overlay.Faint = lipgloss.NewStyle().Faint(true)
	s.Overlay.Error = lipgloss.NewStyle().Foreground(colours.Red)

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

		var color color.Color
		if focused {
			color = colours.Blue
		} else {
			color = colours.Fg
		}

		color = overlayDim(color)

		style = style.BorderForeground(color)

		return style.Padding(0, pad).Foreground(overlayDim(colours.Fg))
	}
	s.TabGap = func(focused bool) lipgloss.Style {
		var color color.Color
		if focused {
			color = colours.Blue
		} else {
			color = colours.Fg
		}

		color = overlayDim(color)

		return lipgloss.NewStyle().
			Border(inactiveTabBorder, true).
			BorderTop(false).
			BorderLeft(false).
			BorderRight(false).
			BorderForeground(color)
	}

	s.NormalBorder = func(focused bool) lipgloss.Style {
		var color color.Color
		if focused {
			color = colours.Blue
		} else {
			color = colours.Fg
		}

		color = overlayDim(color)

		return lipgloss.NewStyle().Border(lipgloss.RoundedBorder()).BorderForeground(color)
	}
	s.OverlayBorder = lipgloss.NewStyle().Border(lipgloss.RoundedBorder()).BorderForeground(colours.Cyan)

	s.Button = func(active, focused bool) lipgloss.Style {
		style := lipgloss.NewStyle().Padding(0, 1)

		if active {
			style = style.Foreground(overlayDim(lipgloss.Color("#fff7db"))).
				Background(overlayDim(lipgloss.Color("#888b7e")))
		} else {
			style = style.Foreground(overlayDim(lipgloss.Color("#a9a9a9"))).
				Background(overlayDim(lipgloss.Color("#555555")))
		}

		if focused {
			style = style.Italic(true).Underline(true)
		}

		return style
	}
	s.DropdownButton = func(active, focused bool, label string, width, marginLeft int) string {
		var fg, bg color.Color
		if active {
			fg = overlayDim(lipgloss.Color("#fff7db"))
			bg = overlayDim(lipgloss.Color("#888b7e"))
		} else {
			fg = overlayDim(lipgloss.Color("#a9a9a9"))
			bg = overlayDim(lipgloss.Color("#555555"))
		}

		labelStyle := lipgloss.NewStyle().
			PaddingLeft(1).
			Foreground(fg).
			Background(bg).
			Width(width)
		if focused {
			labelStyle = labelStyle.Italic(true).Underline(true)
		}

		caretStyle := lipgloss.NewStyle().
			PaddingRight(1).
			Foreground(fg).
			Background(bg)

		combined := lipgloss.JoinHorizontal(
			lipgloss.Top,
			labelStyle.Render(label),
			caretStyle.Render("▼"),
		)

		return lipgloss.NewStyle().MarginLeft(marginLeft).Render(combined)
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

	s.LoadSection.LabelMissing = lipgloss.NewStyle().Foreground(overlayDim(colours.Red))
	s.LoadSection.LabelPending = lipgloss.NewStyle().Foreground(overlayDim(colours.Yellow))
	s.LoadSection.LabelLoaded = lipgloss.NewStyle().Foreground(overlayDim(colours.Green))
	s.LoadSection.LabelSep = lipgloss.NewStyle().Foreground(overlayDim(lipgloss.Lighten(colours.Bg, 0.3)))

	s.SessionPage.Correct = lipgloss.NewStyle().Bold(true).Foreground(colours.Green)
	s.SessionPage.Incorrect = lipgloss.NewStyle().Bold(true).Foreground(colours.Red)

	s.MultipleChoice.Option = func(focused bool, color color.Color) lipgloss.Style {
		borderColor := color
		if focused {
			if color == colours.Fg {
				borderColor = lipgloss.Lighten(colours.Blue, 0.2)
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
	s.MultipleChoice.Unanswered = colours.Fg
	s.MultipleChoice.Correct = colours.Green
	s.MultipleChoice.Incorrect = colours.Red

	s.Dropdown.Item = func(selected bool) lipgloss.Style {
		if selected {
			return lipgloss.NewStyle().Background(lipgloss.Color("#a7a7a7")).Padding(0, 1)
		}
		return lipgloss.NewStyle().Background(lipgloss.Color("#707070")).Padding(0, 1)
	}

	s.ErrorDialog.Border = lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(colours.Red)
	s.ErrorDialog.Header = lipgloss.NewStyle().
		Foreground(colours.Red).
		Bold(true).
		Padding(0, 1).
		Border(lipgloss.NormalBorder(), false, false, true, false).
		BorderForeground(colours.Red)

	s.Filepicker = filepicker.DefaultStyles()
	s.Filepicker.Cursor = lipgloss.NewStyle().Foreground(colours.Pink)
	s.Filepicker.Symlink = lipgloss.NewStyle().Foreground(colours.Green)
	s.Filepicker.Directory = lipgloss.NewStyle().Foreground(colours.Purple)
	s.Filepicker.EmptyDirectory = s.Filepicker.EmptyDirectory.SetString("No files found.")
	s.Filepicker.Selected = s.Filepicker.Selected.Foreground(colours.Pink)

	s.Editor.Theme = goeditor.DefaultTheme(theme.Dark)
	s.Editor.NormalModeStyle = s.Editor.NormalModeStyle.Background(overlayDim(colours.Cyan))
	s.Editor.InsertModeStyle = s.Editor.InsertModeStyle.Background(overlayDim(colours.Blue))
	s.Editor.StatusLineStyle = s.Editor.StatusLineStyle.Foreground(overlayDim(theme.Fg))
	s.Editor.CurrentLineNumberStyle = s.Editor.CurrentLineNumberStyle.Foreground(overlayDim(theme.Fg))
	styleEntryVocab := chromatint.StyleEntry(theme, false)
	styleEntryVocab[chroma.GenericHeading] = fmt.Sprintf("bold %s", hexColor(overlayDim(colours.Orange)))
	styleEntryVocab[chroma.GenericStrong] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: overlayDim(colours.Fg), Bold: true},
		theme.Dark,
	)
	styleEntryVocab[chroma.Comment] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: overlayDim(lipgloss.Lighten(colours.Bg, 0.3)), Italic: true},
		theme.Dark,
	)
	styleEntryVocab[chroma.CommentPreproc] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: overlayDim(lipgloss.Lighten(colours.Bg, 0.3))},
		theme.Dark,
	)
	styleEntryVocab[chroma.Punctuation] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: overlayDim(lipgloss.Darken(colours.Fg, 0.3))},
		theme.Dark,
	)
	styleEntryVocab[chroma.Name] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: overlayDim(colours.Fg)},
		theme.Dark,
	)
	s.Editor.Chroma = chroma.MustNewStyle("bubbletint_vocabeditor", styleEntryVocab)

	s.Form = huh.ThemeFunc(func(isDark bool) *huh.Styles {
		fs := huh.ThemeCharm(theme.Dark)
		fs.Focused.Title = fs.Focused.Title.Foreground(overlayDim(colours.Purple))
		fs.Focused.NoteTitle = fs.Focused.NoteTitle.Foreground(overlayDim(colours.Purple))
		fs.Focused.Directory = fs.Focused.Directory.Foreground(overlayDim(colours.Purple))
		fs.Focused.ErrorIndicator = fs.Focused.ErrorIndicator.Foreground(overlayDim(colours.Red))
		fs.Focused.ErrorMessage = fs.Focused.ErrorMessage.Foreground(overlayDim(colours.Red))
		fs.Focused.SelectSelector = fs.Focused.SelectSelector.Foreground(overlayDim(colours.Pink))
		fs.Focused.NextIndicator = fs.Focused.NextIndicator.Foreground(overlayDim(colours.Pink))
		fs.Focused.PrevIndicator = fs.Focused.PrevIndicator.Foreground(overlayDim(colours.Pink))
		fs.Focused.MultiSelectSelector = fs.Focused.MultiSelectSelector.Foreground(overlayDim(colours.Pink))
		fs.Focused.SelectedOption = fs.Focused.SelectedOption.Foreground(overlayDim(colours.Green))
		fs.Focused.SelectedPrefix = fs.Focused.SelectedPrefix.Foreground(overlayDim(colours.Green))
		fs.Focused.UnselectedOption = fs.Focused.UnselectedOption.Foreground(overlayDim(colours.Fg))
		fs.Focused.FocusedButton = fs.Focused.FocusedButton.
			Foreground(overlayDim(colours.Bg)).
			Background(overlayDim(colours.Pink))
		fs.Focused.BlurredButton = fs.Focused.BlurredButton.
			Foreground(overlayDim(colours.Fg)).
			Background(overlayDim(colours.Bg))

		fs.Focused.TextInput.Cursor = fs.Focused.TextInput.Cursor.Foreground(lipgloss.Color("#f2d5cf"))
		fs.Focused.TextInput.Placeholder = fs.Focused.TextInput.Placeholder.Foreground(
			lipgloss.Lighten(colours.Bg, 0.2),
		)
		fs.Focused.TextInput.Prompt = fs.Focused.TextInput.Prompt.Foreground(colours.Pink)

		fs.Blurred = fs.Focused
		fs.Blurred.Base = fs.Blurred.Base.BorderStyle(lipgloss.HiddenBorder())
		fs.Blurred.Card = fs.Blurred.Base

		fs.Group.Title = fs.Focused.Title
		fs.Group.Description = fs.Focused.Description

		return fs
	})

	styleEntryJSON := chromatint.StyleEntry(theme, false)
	styleEntryJSON[chroma.NameTag] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: overlayDim(colours.Purple)},
		theme.Dark,
	)
	styleEntryJSON[chroma.KeywordConstant] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: overlayDim(colours.Orange)},
		theme.Dark,
	)
	styleEntryJSON[chroma.LiteralNumberInteger] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: overlayDim(colours.Orange)},
		theme.Dark,
	)
	styleEntryJSON[chroma.Punctuation] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: overlayDim(colours.Fg)},
		theme.Dark,
	)
	s.Jsonview = chroma.MustNewStyle("bubbletint_json", styleEntryJSON)

	s.Fang = func(lightDark lipgloss.LightDarkFunc) fang.ColorScheme {
		// NOTE: Using closest equivalents in the theme for the charmtone colours
		cs := fang.DefaultColorScheme(lightDark)
		cs.Title = colours.Purple                                // ct.Charple
		cs.Program = colours.Blue                                // ld(ct.Malibu, ct.Guppy) (fsr these colours are completely different, using Malibu)
		cs.Command = colours.Pink                                // ld(ct.Pony, ct.Cheeky)
		cs.Flag = colours.Green                                  // ld(lipgloss.Color("#0CB37F"), ct.Guac)
		cs.QuotedString = colours.Coral                          // ld(ct.Coral, charmtone.Salmon)
		cs.ErrorHeader = [2]color.Color{colours.Bg, colours.Red} // ct.Butter, ct.Cherry
		return cs
	}

	return s
}
