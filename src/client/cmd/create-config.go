package cmd

import (
	"fmt"

	"github.com/spf13/cobra"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
)

var createConfigCmd = &cobra.Command{
	Version: internal.Version,
	Use:     "create-config",
	Short:   "Create a session config for the vocab tester.",
	Long: `Create a session config for the vocab tester.
Starts a wizard that receives input from the user on each setting and generates a config file.`,
	Run: func(cmd *cobra.Command, args []string) { //nolint:revive
		fmt.Printf("Config wizard.")
	},
}

func init() {
	rootCmd.AddCommand(createConfigCmd)
}
