package cmd

import (
	"fmt"
	"os"

	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/spf13/cobra"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
	"github.com/rduo1009/vocab-tuister/src/client/internal/listtui"
)

var ListPath string

var createListCmd = &cobra.Command{
	Version: internal.Version,
	Use:     "create-list",
	Short:   "Write a list for the vocab tester.",
	Long: `Write a list for the vocab tester.
The user will have to write the list out manually.`,
	Run: func(cmd *cobra.Command, args []string) { //nolint:revive
		if len(args) != 1 {
			fmt.Println("Invalid number of arguments given. (expected 1)")
			os.Exit(1)
		}

		listPath := args[0]

		p := tea.NewProgram(listtui.InitialModel(listPath))
		if _, err := p.Run(); err != nil {
			fmt.Println(err)
			os.Exit(1)
		}
	},
}

func init() {
	rootCmd.AddCommand(createListCmd)
}
