package styles

import (
	tint "github.com/lrstanley/bubbletint/v2"
)

// TODO: Light themes!
func DefaultThemes(isDark bool) *tint.Registry {
	if isDark {
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
		)
	}

	// NOTE: Using closest equivalents here
	return tint.NewRegistry(
		tint.TintCatppuccinLatte, // reasonable default
		tint.TintTokyoNightLight,
		// tint.TintDraculaPlus, // XXX: Light mode?
		tint.TintGruvboxLight,
		tint.TintBuiltinSolarizedLight,
		tint.TintNordLight,
		// tint.TintMonokaiPro,
		tint.TintOneHalfLight,
		tint.TintMaterial,
		tint.TintKanagawa,
		tint.TintRosePineDawn,
	)
}
