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

func hexColor(c color.Color) string {
	rgba := color.RGBAModel.Convert(c).(color.RGBA)
	return fmt.Sprintf("#%.2x%.2x%.2x", rgba.R, rgba.G, rgba.B)
}

func DefaultStyles(theme *tint.Tint) Styles {
	colours := DefaultColours(theme)

	s := Styles{}

	s.Title = lipgloss.NewStyle().Bold(true).Underline(true)
	s.Bold = lipgloss.NewStyle().Bold(true)
	s.Italic = lipgloss.NewStyle().Italic(true)
	s.Faint = lipgloss.NewStyle().Faint(true)
	s.Error = lipgloss.NewStyle().Foreground(colours.Red)

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
			style = style.BorderForeground(colours.Blue)
		} else {
			style = style.BorderForeground(colours.Fg)
		}

		return style.Padding(0, pad)
	}
	s.TabGap = func(focused bool) lipgloss.Style {
		style := lipgloss.NewStyle().Border(inactiveTabBorder, true)
		if focused {
			style = style.BorderForeground(colours.Blue)
		} else {
			style = style.BorderForeground(colours.Fg)
		}

		return style.BorderTop(false).
			BorderLeft(false).
			BorderRight(false)
	}

	s.NormalBorder = func(focused bool) lipgloss.Style {
		if focused {
			return lipgloss.NewStyle().Border(lipgloss.RoundedBorder()).BorderForeground(colours.Blue)
		}
		return lipgloss.NewStyle().Border(lipgloss.RoundedBorder()).BorderForeground(colours.Fg)
	}
	s.OverlayBorder = lipgloss.NewStyle().Border(lipgloss.RoundedBorder()).BorderForeground(colours.Cyan)

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

	s.LoadSection.LabelMissing = lipgloss.NewStyle().Foreground(colours.Red)
	s.LoadSection.LabelPending = lipgloss.NewStyle().Foreground(colours.Yellow)
	s.LoadSection.LabelLoaded = lipgloss.NewStyle().Foreground(colours.Green)
	s.LoadSection.LabelSep = lipgloss.NewStyle().Foreground(lipgloss.Lighten(colours.Bg, 0.3))

	s.SessionPage.Correct = lipgloss.NewStyle().Bold(true).Foreground(colours.Green)
	s.SessionPage.Incorrect = lipgloss.NewStyle().Bold(true).Foreground(colours.Red)

	s.MultipleChoice.Option = func(focused bool, color color.Color) lipgloss.Style {
		borderColor := color
		if focused {
			if color == colours.Fg {
				borderColor = colours.Pink
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
	s.Editor.NormalModeStyle = s.Editor.NormalModeStyle.Background(colours.Cyan)
	s.Editor.InsertModeStyle = s.Editor.InsertModeStyle.Background(colours.Blue)
	styleEntryVocab := chromatint.StyleEntry(theme, false)
	styleEntryVocab[chroma.GenericHeading] = fmt.Sprintf("bold %s", hexColor(colours.Orange))
	styleEntryVocab[chroma.GenericStrong] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: colours.Fg, Bold: true},
		theme.Dark,
	)
	styleEntryVocab[chroma.Comment] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: lipgloss.Lighten(colours.Bg, 0.3), Italic: true},
		theme.Dark,
	)
	styleEntryVocab[chroma.CommentPreproc] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: lipgloss.Lighten(colours.Bg, 0.3)},
		theme.Dark,
	)
	s.Editor.Chroma = chroma.MustNewStyle("bubbletint_vocabeditor", styleEntryVocab)

	s.Form = huh.ThemeFunc(func(isDark bool) *huh.Styles {
		formStyles := huh.ThemeCharm(theme.Dark)
		formStyles.Focused.Title = formStyles.Focused.Title.Foreground(colours.Purple)
		formStyles.Focused.NoteTitle = formStyles.Focused.NoteTitle.Foreground(colours.Purple)
		formStyles.Focused.Directory = formStyles.Focused.Directory.Foreground(colours.Purple)
		formStyles.Focused.ErrorIndicator = formStyles.Focused.ErrorIndicator.Foreground(colours.Red)
		formStyles.Focused.ErrorMessage = formStyles.Focused.ErrorMessage.Foreground(colours.Red)
		formStyles.Focused.SelectSelector = formStyles.Focused.SelectSelector.Foreground(colours.Pink)
		formStyles.Focused.NextIndicator = formStyles.Focused.NextIndicator.Foreground(colours.Pink)
		formStyles.Focused.PrevIndicator = formStyles.Focused.PrevIndicator.Foreground(colours.Pink)
		formStyles.Focused.MultiSelectSelector = formStyles.Focused.MultiSelectSelector.Foreground(colours.Pink)
		formStyles.Focused.SelectedOption = formStyles.Focused.SelectedOption.Foreground(colours.Green)
		formStyles.Focused.SelectedPrefix = formStyles.Focused.SelectedPrefix.Foreground(colours.Green)
		formStyles.Focused.UnselectedOption = formStyles.Focused.UnselectedOption.Foreground(colours.Fg)
		formStyles.Focused.FocusedButton = formStyles.Focused.FocusedButton.Foreground(colours.Bg).
			Background(colours.Pink)
		formStyles.Focused.BlurredButton = formStyles.Focused.BlurredButton.Foreground(colours.Fg).
			Background(colours.Bg)

		formStyles.Focused.TextInput.Cursor = formStyles.Focused.TextInput.Cursor.Foreground(
			lipgloss.Color("#f2d5cf"),
		)
		formStyles.Focused.TextInput.Placeholder = formStyles.Focused.TextInput.Placeholder.Foreground(
			lipgloss.Lighten(colours.Bg, 0.2),
		)
		formStyles.Focused.TextInput.Prompt = formStyles.Focused.TextInput.Prompt.Foreground(colours.Pink)

		formStyles.Blurred = formStyles.Focused
		formStyles.Blurred.Base = formStyles.Blurred.Base.BorderStyle(lipgloss.HiddenBorder())
		formStyles.Blurred.Card = formStyles.Blurred.Base

		formStyles.Group.Title = formStyles.Focused.Title
		formStyles.Group.Description = formStyles.Focused.Description

		return formStyles
	})

	styleEntryJSON := chromatint.StyleEntry(theme, false)
	styleEntryJSON[chroma.NameTag] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: colours.Purple},
		theme.Dark,
	)
	styleEntryJSON[chroma.LiteralNumber] = chromatint.FromStyle(
		&chromatint.StaticStyle{Fg: colours.Orange},
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
