package schema

import (
	"fmt"
	"strings"
)

//go:tag mkunion:"Location"
type (
	LocationField struct {
		Name string
	}
	LocationIndex struct {
		Index int
	}
	LocationAnything struct{}
)

func LocationToStr(location []Location) string {
	var result string
	for _, l := range location {
		result += MatchLocationR1(
			l,
			func(x *LocationField) string {
				if strings.Contains(x.Name, ".") ||
					strings.Contains(x.Name, "$") {
					return fmt.Sprintf(`["%s"]`, x.Name)
				}
				return "." + x.Name
			},
			func(x *LocationIndex) string {
				return fmt.Sprintf("[%d]", x.Index)
			},
			func(x *LocationAnything) string {
				return "[*]"
			},
		)
	}

	return strings.Trim(result, ".")
}
