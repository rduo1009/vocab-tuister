package pages

import (
	"fmt"

	"github.com/rduo1009/vocab-tuister/src/client/internal/styles"
)

//go:generate go tool stringer -type=PageName -output=pagename_string_gen.go
type PageName int

const (
	Create PageName = iota
	Review
	Test
	Help
	Settings
)

func (p PageName) DisplayString(styles *styles.StylesWrapper) string {
	pageNameIcons := map[PageName]string{
		Create:   styles.Icons.PencilSquare,
		Review:   styles.Icons.Book,
		Test:     styles.Icons.Bullseye,
		Help:     styles.Icons.Info,
		Settings: styles.Icons.Cog,
	}

	if pageNameIcons[p] == "" {
		return p.String()
	} else {
		return fmt.Sprintf("%s %s", pageNameIcons[p], p.String())
	}
}
