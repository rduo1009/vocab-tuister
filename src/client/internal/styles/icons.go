package styles

import (
	"context"
	"time"

	"github.com/lrstanley/go-nf"
	"github.com/lrstanley/go-nf/glyphs/cod"
	"github.com/lrstanley/go-nf/glyphs/fa"
	"github.com/lrstanley/go-nf/glyphs/md"
	"github.com/lrstanley/go-nf/glyphs/oct"
)

var hasNerdFonts bool

type Icons struct {
	HasNerdFonts bool

	PencilSquare string // 'Create' tab
	Book         string // 'Review' tab
	Bullseye     string // 'Test' tab
	Info         string // 'Help' tab
	Cog          string // 'Settings' tab

	Checkmark string
	Cross     string

	CrossCircle string // Error dialog
}

func DefaultIcons() *Icons {
	if hasNerdFonts {
		return defaultIconsWithNerdFont()
	}
	return defaultIconsWithoutNerdFont()
}

func defaultIconsWithNerdFont() *Icons {
	return &Icons{
		HasNerdFonts: true,

		PencilSquare: fa.PencilSquare.String(),
		Book:         cod.Book.String(),
		Bullseye:     md.BullseyeArrow.String(),
		Info:         md.InformationOutline.String(),
		Cog:          md.Cog.String(),

		Checkmark: md.Check.String(),
		Cross:     oct.X.String(),

		CrossCircle: fa.CircleXmark.String(),
	}
}

func defaultIconsWithoutNerdFont() *Icons {
	return &Icons{
		HasNerdFonts: false,

		// If nerd fonts are not used then there should be no tab icons
		PencilSquare: "",
		Book:         "",
		Bullseye:     "",
		Info:         "",
		Cog:          "",

		Checkmark: "✓",
		Cross:     "✕",

		CrossCircle: "ⓧ",
	}
}

func init() {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	status, err := nf.DetectInstalled(ctx)
	if err != nil {
		return
	}

	switch status {
	case nf.StatusEnabled, nf.StatusInstalled:
		hasNerdFonts = true
	case nf.StatusDisabled, nf.StatusNotInstalled:
		hasNerdFonts = false
	}
}
