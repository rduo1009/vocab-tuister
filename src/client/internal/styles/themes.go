package styles

import (
	tint "github.com/lrstanley/bubbletint/v2"
)

func DefaultThemes() *tint.Registry {
	return tint.NewRegistry(
		tint.TintCatppuccinMocha, // reasonable default
		tint.TintTokyoNight,
		tint.TintDraculaPlus,
		tint.TintGruvboxDark,
		tint.TintBuiltinSolarizedDark,
		tint.TintNord,
		tint.TintMonokaiPro,
		tint.TintOneDark,
		tint.TintMaterialDark,
		tint.TintKanagawa,
		tint.TintRosePine,
		// TODO: Add more!
	)
}
