package cmd

import (
	tea "github.com/charmbracelet/bubbletea"
	"github.com/spf13/cobra"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
	"github.com/rduo1009/vocab-tuister/src/client/internal/configtui"
)

var createConfigCmd = &cobra.Command{
	Version: internal.Version,
	Use:     "create-config [file to write to]",
	Short:   "Create a session config for the vocab tester.",
	Long: `Create a session config for the vocab tester.
Starts a wizard that receives input from the user on each setting and generates a config file.`,

	Args: func(cmd *cobra.Command, args []string) error {
		if err := cobra.ExactArgs(1)(cmd, args); err != nil {
			return err
		}
		return nil
	},

	RunE: func(cmd *cobra.Command, args []string) error { //nolint:revive
		listPath := args[0]

		p := tea.NewProgram(configtui.InitialModel(listPath))
		if _, err := p.Run(); err != nil {
			return err
		}

		return nil
	},
}

func init() {
	rootCmd.AddCommand(createConfigCmd)
}
