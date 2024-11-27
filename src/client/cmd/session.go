package cmd

import (
	"fmt"

	"github.com/rduo1009/vocab-tuister/src/client/internal"
	"github.com/spf13/cobra"
)

var sessionCmd = &cobra.Command{
	Version: internal.Version,
	Use:     "session",
	Short:   "Starts a testing session.",
	Long: `Starts a testing session.
This is based on the vocab list and the session config file provided.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("Session started.")
	},
}

func init() {
	rootCmd.AddCommand(sessionCmd)
}
