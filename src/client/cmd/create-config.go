package cmd

import (
	"fmt"
	"os"

	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/spf13/cobra"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
	"github.com/rduo1009/vocab-tuister/src/client/internal/configtui"
)

var createConfigCmd = &cobra.Command{
	Version: internal.Version,
	Use:     "create-config",
	Short:   "Create a session config for the vocab tester.",
	Long: `Create a session config for the vocab tester.
Starts a wizard that receives input from the user on each setting and generates a config file.`,
	Run: func(cmd *cobra.Command, args []string) { //nolint:revive
		if len(args) != 1 {
			fmt.Println("Invalid number of arguments given. (expected 1)")
			os.Exit(1)
		}

		listPath := args[0]

		p := tea.NewProgram(configtui.InitialModel(listPath))
		if _, err := p.Run(); err != nil {
			fmt.Println(err)
			os.Exit(1)
		}
	},
}

func init() {
	rootCmd.AddCommand(createConfigCmd)
}
