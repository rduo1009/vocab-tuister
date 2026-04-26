package pages

//go:generate go tool stringer -type=PageName -output=pagename_string_gen.go
type PageName int

const (
	Create PageName = iota
	Review
	Test
	Help
	Settings
)
