/*
Copyright © 2025 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"fmt"
	"os/exec"
	"strconv"

	"github.com/spf13/cobra"
)

// runCmd represents the run command
var runCmd = &cobra.Command{
	Use:   "run",
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {

		size, _ := cmd.Flags().GetInt("size")
		hillsNumber, _ := cmd.Flags().GetInt("hills")
		wrecksNumber, _ := cmd.Flags().GetInt("wrecks")

		fmt.Printf("Running simulation with size:%d, hills:%d, wrecks:%d\n", size, hillsNumber, wrecksNumber)

		pythonScript := exec.Command("python3", "./python/main.py", strconv.Itoa(size), strconv.Itoa(hillsNumber),
			strconv.Itoa(wrecksNumber))
		_, err := pythonScript.Output()

		if err != nil {
			fmt.Println(err)
		}

		// to do: dodać zapis do bazy danych
	},
}

func init() {
	rootCmd.AddCommand(runCmd)

	// Here you will define your flags and configuration settings.
	runCmd.Flags().Int("size", 1000, "Seafloor size")
	runCmd.Flags().Int("hills", 8, "Number of hills")
	runCmd.Flags().Int("wrecks", 8, "Number of wrecks")

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// runCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// runCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
