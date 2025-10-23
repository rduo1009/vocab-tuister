package create

import "github.com/charmbracelet/bubbles/v2/help"

// KeyMap helps satisfy the StringViewModel interface. It returns the help.KeyMap of the focused component.
//
// It should never be ran in the root model - the KeyMap functions of the subcomponents should be preferred.
func (m *Model) KeyMap() help.KeyMap {
	panic("not implemented")
}
