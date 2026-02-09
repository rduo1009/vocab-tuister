package util

import tea "charm.land/bubbletea/v2"

// --- Value Receiver Version ---

// updatableVal defines a component where Update returns a new copy of the model.
// This is typical for small, immutable-style models like textinput.
type updatableVal[M any] interface {
	Update(tea.Msg) (M, tea.Cmd)
}

// UpdaterVal is used when your model is stored as a value (e.g., m.textinput).
// It reassigns the returned model to the pointer provided.
func UpdaterVal[M updatableVal[M]](cmds *[]tea.Cmd, toUpdate *M, msg tea.Msg) {
	updated, cmd := (*toUpdate).Update(msg)
	if cmd != nil {
		*cmds = append(*cmds, cmd)
	}

	*toUpdate = updated
}

// --- Pointer Receiver Version ---

// updatablePtr defines a component where the Update method is called on a pointer.
// R is the return type of the Update method (often the pointer itself or an interface).
type updatablePtr[R any] interface {
	Update(tea.Msg) (R, tea.Cmd)
}

// UpdaterPtr is used when your model is already a pointer (e.g., m.listtui).
// Since the receiver is a pointer, it updates the state in-place.
func UpdaterPtr[R any, M updatablePtr[R]](cmds *[]tea.Cmd, toUpdate M, msg tea.Msg) {
	// We ignore the first return because pointer receivers modify the object directly.
	_, cmd := toUpdate.Update(msg)
	if cmd != nil {
		*cmds = append(*cmds, cmd)
	}
}
