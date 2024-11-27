package cmd

import (
	"fmt"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
	"github.com/spf13/cobra"
)

var createListCmd = &cobra.Command{
	Version: internal.Version,
	Use:     "create-list",
	Short:   "Write a list for the vocab tester.",
	Long: `Write a list for the vocab tester.
The user will have to write the list out manually.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("List creator.")
	},
}

func init() {
	rootCmd.AddCommand(createListCmd)
}
