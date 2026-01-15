// Package vimtea provides a Vim-like text editor component for terminal applications
package vimtea

import tea "github.com/charmbracelet/bubbletea/v2"

// Command is a function that performs an action on the editor model
// and returns a bubbletea command.
type Command func(m *editorModel) tea.Cmd

// KeyBinding represents a key binding that can be registered with the editor
// This is the public API for adding key bindings.
type KeyBinding struct {
	Key         string               // The key sequence to bind (e.g. "j", "dd", "ctrl+f")
	Mode        EditorMode           // Which editor mode this binding is active in
	Description string               // Human-readable description for help screens
	Handler     func(Buffer) tea.Cmd // Function to execute when the key is pressed
}

// UndoRedoMsg is sent when an undo or redo operation is performed
// It contains the new cursor position and operation status.
type UndoRedoMsg struct {
	NewCursor Cursor // New cursor position after undo/redo
	Success   bool   // Whether the operation succeeded
	IsUndo    bool   // True for undo, false for redo
}

// internalKeyBinding is the internal representation of a key binding
// used by the binding registry.
type internalKeyBinding struct {
	Key     string     // The key sequence
	Command Command    // The command function to execute
	Mode    EditorMode // The editor mode this binding is active in
	Help    string     // Help text describing the binding
}

// CommandRegistry stores and manages commands that can be executed in command mode
// Commands are invoked by typing ":command" in command mode.
type CommandRegistry struct {
	commands map[string]Command // Map of command names to command functions
}

// BindingRegistry manages key bindings for the editor
// It supports exact matches and prefix detection for multi-key sequences.
type BindingRegistry struct {
	// Maps EditorMode -> key sequence -> binding
	exactBindings map[EditorMode]map[string]internalKeyBinding

	// Maps EditorMode -> key prefix -> true
	// Used to detect if a key sequence could be a prefix of a longer binding
	prefixBindings map[EditorMode]map[string]bool

	// List of all bindings for help display
	allBindings []internalKeyBinding
}

// newBindingRegistry creates a new empty binding registry.
func newBindingRegistry() *BindingRegistry {
	return &BindingRegistry{
		exactBindings:  make(map[EditorMode]map[string]internalKeyBinding),
		prefixBindings: make(map[EditorMode]map[string]bool),
		allBindings:    []internalKeyBinding{},
	}
}

// newCommandRegistry creates a new empty command registry.
func newCommandRegistry() *CommandRegistry {
	return &CommandRegistry{
		commands: make(map[string]Command),
	}
}

// Add registers a new key binding with the registry
// It automatically builds prefix maps for multi-key sequences.
func (r *BindingRegistry) Add(key string, cmd Command, mode EditorMode, help string) {
	binding := internalKeyBinding{
		Key:     key,
		Command: cmd,
		Mode:    mode,
		Help:    help,
	}

	// Initialize mode map if needed
	if r.exactBindings[mode] == nil {
		r.exactBindings[mode] = make(map[string]internalKeyBinding)
	}
	r.exactBindings[mode][key] = binding

	// Initialize prefix map if needed
	if r.prefixBindings[mode] == nil {
		r.prefixBindings[mode] = make(map[string]bool)
	}

	// Register all prefixes of the key sequence
	// For example, for "dw", register "d" as a prefix
	for i := 1; i < len(key); i++ {
		prefix := key[:i]
		r.prefixBindings[mode][prefix] = true
	}

	// Add to the list of all bindings
	r.allBindings = append(r.allBindings, binding)
}

// FindExact looks for an exact match for the given key sequence in the specified mode
// It can handle numeric prefixes by ignoring them when looking for the command.
func (r *BindingRegistry) FindExact(keySeq string, mode EditorMode) *internalKeyBinding {
	// Find where the numeric prefix ends (if any)
	nonDigitStart := 0
	for i, c := range keySeq {
		if c < '0' || c > '9' {
			nonDigitStart = i
			break
		}
	}

	// If the sequence is all digits, it's not a command
	if nonDigitStart == len(keySeq) {
		return nil
	}

	// Try to match without the numeric prefix
	cmdPart := keySeq[nonDigitStart:]
	if modeBindings, ok := r.exactBindings[mode]; ok {
		if binding, ok := modeBindings[cmdPart]; ok {
			return &binding
		}
	}

	// Try to match the full sequence (including any numeric prefix)
	if modeBindings, ok := r.exactBindings[mode]; ok {
		if binding, ok := modeBindings[keySeq]; ok {
			return &binding
		}
	}

	return nil
}

// IsPrefix checks if the key sequence is a prefix of any registered binding
// This is used to determine if we should wait for more input.
func (r *BindingRegistry) IsPrefix(keySeq string, mode EditorMode) bool {
	if prefixes, ok := r.prefixBindings[mode]; ok {
		return prefixes[keySeq]
	}
	return false
}

// GetAll returns all registered key bindings.
func (r *BindingRegistry) GetAll() []internalKeyBinding {
	return r.allBindings
}

// GetForMode returns all key bindings for the specified mode.
func (r *BindingRegistry) GetForMode(mode EditorMode) []internalKeyBinding {
	var result []internalKeyBinding
	for _, binding := range r.allBindings {
		if binding.Mode == mode {
			result = append(result, binding)
		}
	}
	return result
}

// Register adds a command to the registry with the given name.
func (r *CommandRegistry) Register(name string, cmd Command) {
	r.commands[name] = cmd
}

// Get retrieves a command by name, returning nil if not found.
func (r *CommandRegistry) Get(name string) Command {
	cmd, ok := r.commands[name]
	if !ok {
		return nil
	}
	return cmd
}

// GetAll returns all registered commands as a map.
func (r *CommandRegistry) GetAll() map[string]Command {
	return r.commands
}
