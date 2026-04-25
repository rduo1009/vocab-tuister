package config

import (
	"encoding/json/jsontext"
	"encoding/json/v2"
	"fmt"
	"os"
	"reflect"
	"strconv"
	"strings"
	"unsafe"

	"charm.land/bubbles/v2/key"
	tea "charm.land/bubbletea/v2"
	"charm.land/huh/v2"

	"github.com/rduo1009/vocab-tuister/src/client/internal/app"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/filepicker"
	"github.com/rduo1009/vocab-tuister/src/client/internal/components/navigator"
	"github.com/rduo1009/vocab-tuister/src/client/internal/util"
)

type configMap map[string]any

type (
	formSubmittedMsg    struct{}
	rawSessionConfigMsg []byte

	// In case there is an error with `generateSessionConfig` to distinguish with `app.ErrMsg`.
	failFormMsg struct{}
)

func generateSessionConfig(values *formValues) tea.Cmd {
	generate := func() ([]byte, error) {
		configMap := make(configMap)

		allSelections := [][]string{
			values.PartsOfSpeechExclusions,
			values.VerbExclusions,
			values.ParticipleExclusions,
			values.OtherVerbExclusions,
			values.NounExclusions,
			values.AdjectiveExclusions,
			values.AdverbExclusions,
			values.PronounExclusions,
			values.RegularExclusions,
			values.Miscellaneous,
			values.QuestionTypes,
		}

		selected := make(map[string]struct{})
		for _, selections := range allSelections {
			for _, key := range selections {
				selected[key] = struct{}{}
			}
		}

		for _, key := range allKeys {
			_, ok := selected[key]
			configMap[key] = ok
		}

		numberMultipleChoiceOptions, err := strconv.Atoi(values.NumberMultipleChoiceOptionsString)
		if err != nil {
			return nil, fmt.Errorf(
				"failed to convert %s to integer: %w",
				values.NumberMultipleChoiceOptionsString,
				err,
			)
		}

		configMap["number-multiplechoice-options"] = numberMultipleChoiceOptions

		numberOfQuestions, err := strconv.Atoi(values.NumberOfQuestionsString)
		if err != nil {
			return nil, fmt.Errorf(
				"failed to convert %s to integer: %w",
				values.NumberOfQuestionsString,
				err,
			)
		}

		configMap["number-of-questions"] = numberOfQuestions

		data, err := json.Marshal(configMap)
		if err != nil {
			return nil, fmt.Errorf("failed to marshal session config: %w", err)
		}

		// Convert to Value and canonicalize to maintain alphabetical key ordering
		value := jsontext.Value(data)

		err = value.Canonicalize(
			jsontext.WithIndent("  "),
			jsontext.SpaceAfterColon(true),
			jsontext.SpaceAfterComma(false),
		)
		if err != nil {
			return nil, fmt.Errorf("failed to canonicalize json: %w", err)
		}

		return value, nil
	}

	rawSessionConfig, err := generate()
	if err != nil {
		return tea.Batch(util.MsgCmd(app.ErrMsg(err)), util.MsgCmd(failFormMsg{}))
	}

	return util.MsgCmd(rawSessionConfigMsg(rawSessionConfig))
}

func readSessionConfigFile(selectedFile string) tea.Cmd {
	return func() tea.Msg {
		rawSessionConfig, err := os.ReadFile(selectedFile)
		if err != nil {
			return app.ErrMsg(fmt.Errorf("failed to read session config file at %s: %w", selectedFile, err))
		}

		value := jsontext.Value(rawSessionConfig)

		err = value.Canonicalize(jsontext.WithIndent("  "),
			jsontext.SpaceAfterColon(true),
			jsontext.SpaceAfterComma(false),
		)
		if err != nil {
			return app.ErrMsg(fmt.Errorf("failed to canonicalize json: %w", err))
		}

		return rawSessionConfigMsg(value)
	}
}

func (m *Model) Update(msg tea.Msg) (app.ComponentModel, tea.Cmd) {
	var cmds []tea.Cmd

	if m.FilepickerActive {
		switch msg := msg.(type) {
		case app.OverlayMsg:
			m.form.WithTheme(m.styles.Form)
			setFieldThemes(m.form, m.styles.Form)
			util.UpdaterPtr(&cmds, m.form, nil) // nudge
			m.jsonview.Refresh()

		case filepicker.PickedMsg:
			if msg.ID == filepickerID {
				m.FilepickerActive = false

				cmds = append(cmds, readSessionConfigFile(msg.SelectedFile))
			}

		case filepicker.ExitMsg:
			if msg.ID == filepickerID {
				m.FilepickerActive = false
			}
		}

		util.UpdaterPtr(&cmds, m.Filepicker, msg)

		return m, tea.Batch(cmds...)
	}

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		if m.HeaderSection.Focused() && key.Matches(msg, m.HeaderSection.KeyMap().PressButton) {
			m.FilepickerActive = true
			return m, nil
		} else if m.ResetButton.Focused() && key.Matches(msg, m.ResetButton.KeyMap().PressButton) {
			m.form, m.configFormValues = defaultForm()
			m.AppStatus = CreateSessionConfig
			m.RawSessionConfig = ""
			_, formCmd := m.form.Update(nil) // a little nudge

			return m, tea.Batch(
				formCmd,
				util.MsgCmd(navigator.RemoveNavigableMsg{
					Components: []navigator.Navigable{m.ResetButton},
				}),
			)
		}

	case app.OverlayMsg:
		m.form.WithTheme(m.styles.Form)
		setFieldThemes(m.form, m.styles.Form)
		if !m.FormSection.Focused() {
			util.UpdaterPtr(&cmds, m.form, nil)
			m.jsonview.Refresh()
			return m, tea.Batch(cmds...)
		}

	case formSubmittedMsg:
		cmds = append(cmds, generateSessionConfig(m.configFormValues))

	case rawSessionConfigMsg:
		if m.AppStatus == CreateSessionConfig {
			// navigator: [..., HeaderSection, FormSection, ...]
			cmds = append(cmds, tea.Sequence(
				// now navigator: [..., HeaderSection, ResetButton, FormSection, ...]
				util.MsgCmd(navigator.ReplaceNavigableMsg{
					Target:      m.FormSection,
					Replacement: []navigator.Navigable{m.ResetButton, m.FormSection},
				}),
				util.MsgCmd(navigator.FocusNavigableMsg{Target: m.FormSection}),
			))
		} // otherwise, the app status was already `ReviewSessionConfig` and so nothing needs to be done

		m.AppStatus = ReviewSessionConfig
		m.RawSessionConfig = string(msg)
		m.jsonview.SetContent(m.RawSessionConfig)

	case failFormMsg:
		m.form, m.configFormValues = defaultForm()
		m.AppStatus = CreateSessionConfig
		m.RawSessionConfig = ""
		_, formCmd := m.form.Update(nil) // a little nudge

		return m, tea.Batch(
			formCmd,
			util.MsgCmd(navigator.RemoveNavigableMsg{
				Components: []navigator.Navigable{m.ResetButton},
			}),
		)

	default:
		util.UpdaterPtr(&cmds, m.Filepicker, msg)
	}

	if m.FormSection.Focused() {
		if m.AppStatus == CreateSessionConfig {
			util.UpdaterPtr(&cmds, m.form, msg)
		} else {
			util.UpdaterPtr(&cmds, m.jsonview, msg)
		}
	}

	return m, tea.Batch(cmds...)
}

// HACK: Very flimsy and vibe-coded solution to some quirks in huh
// - for some reason, some huh fields cannot have their theme changed after it is first set
//   see (https://github.com/charmbracelet/huh/commit/dadcb82)
// - thankfully, all field structs have the unexported field 'theme' so the theme can still be changed
// - I could have vendored huh and fixed it myself but it wasn't needed in this case.
//   The chance that the internal api changes is very unlikely. (huh project is partially dead)

// getUnexportedField retrieves an unexported field by name using reflect + unsafe.
func getUnexportedField(v reflect.Value, name string) reflect.Value {
	field := v.FieldByName(name)
	// Make the unexported field readable via unsafe
	return reflect.NewAt(field.Type(), unsafe.Pointer(field.UnsafeAddr())).Elem()
}

// setUnexportedField sets an unexported field using reflect + unsafe.
func setUnexportedField(field, value reflect.Value) {
	reflect.NewAt(field.Type(), unsafe.Pointer(field.UnsafeAddr())).
		Elem().
		Set(value)
}

// assertType panics if the type of val is not as expected.
// This is used to detect breaking changes in unexported huh internals —
// if the library renames or restructures its types, the check will fail
// rather than silently producing wrong behaviour.
func assertType(val reflect.Value, expected string) {
	actual := val.Type().String()

	normalized := strings.NewReplacer(
		"charm.land/huh/v2", "huh",
		"charm.land/huh", "huh",
	).Replace(actual)

	if normalized != expected {
		panic(fmt.Sprintf(
			"huh internals changed: expected type %q, got %q (normalized from %q)",
			expected,
			normalized,
			actual,
		))
	}
}

// setFieldThemes overrides the 'theme' attribute of every [huh.Field] of every [huh.Group].
// Of course, this assumes that every field has a 'theme' attribute with type [huh.Theme].
// setFieldThemes will panic if a type is not as expected.
//
// setFieldThemes simulates the following code:
//
//	for _, group := range m.form.selector.items {
//	    for _, field := range group.selector.items {
//	        field.theme = m.styles.Form.Theme
//	    }
//	}
func setFieldThemes(form *huh.Form, theme huh.Theme) {
	// Get the unexported 'selector' field from Form
	formVal := reflect.ValueOf(form).Elem()
	formSelector := getUnexportedField(formVal, "selector")
	assertType(formSelector, "*selector.Selector[*huh.Group]")

	// Get the 'items' slice from the form's selector
	groups := getUnexportedField(formSelector.Elem(), "items")
	assertType(groups, "[]*huh.Group")

	for i := 0; i < groups.Len(); i++ {
		group := groups.Index(i)
		assertType(group, "*huh.Group")

		// Each item is a *Group — dereference it
		groupElem := group.Elem()

		// Get the group's selector field
		groupSelector := getUnexportedField(groupElem, "selector")
		assertType(groupSelector, "*selector.Selector[huh.Field]")

		// Get the 'items' slice from the group's selector
		fields := getUnexportedField(groupSelector.Elem(), "items")
		assertType(fields, "[]huh.Field")

		for j := 0; j < fields.Len(); j++ {
			field := fields.Index(j)
			assertType(field, "huh.Field")

			// Field is an interface (huh.Field), get the concrete value
			fieldConcrete := field.Elem()
			if fieldConcrete.Kind() == reflect.Ptr {
				fieldConcrete = fieldConcrete.Elem()
			}

			// Set the 'theme' field
			themeField := getUnexportedField(fieldConcrete, "theme")
			if themeField.IsValid() {
				setUnexportedField(themeField, reflect.ValueOf(theme))
			}
		}
	}
}
