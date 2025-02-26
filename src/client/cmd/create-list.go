package cmd

import (
	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/spf13/cobra"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
	"github.com/rduo1009/vocab-tuister/src/client/internal/listtui"
)

var ListPath string

var createListCmd = &cobra.Command{
	Version: internal.Version,
	Use:     "create-list [file to write to]",
	Short:   "Write a list for the vocab tester.",
	Long: `Write a list for the vocab tester.
The user will have to write the list out manually.`,

	Args: func(cmd *cobra.Command, args []string) error {
		if err := cobra.ExactArgs(1)(cmd, args); err != nil {
			return err
		}
		return nil
	},

	RunE: func(cmd *cobra.Command, args []string) error { //nolint:revive
		listPath := args[0]

		p := tea.NewProgram(listtui.InitialModel(listPath))
		if _, err := p.Run(); err != nil {
			return err
		}

		return nil
	},
}

func init() {
	rootCmd.AddCommand(createListCmd)
}
