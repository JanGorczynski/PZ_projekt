package cmd

import (
	"encoding/json"
	"fmt"
	"github.com/spf13/cobra"
	"log"
	"oceangate/db"
	"oceangate/models"
	"os"
	"os/exec"
	"strconv"
	"time"
)

var run = &cobra.Command{
	Use:   "run",
	Short: "Run the submarine simulation and store in DB",
	Long:  `Run the submarine simulation and store submarine path data into the database.`,
	Run: func(cmd *cobra.Command, args []string) {

		size, _ := cmd.Flags().GetInt("size")
		hillsNumber, _ := cmd.Flags().GetInt("hills")
		wrecksNumber, _ := cmd.Flags().GetInt("wrecks")
		submarine, _ := cmd.Flags().GetInt("submarine")

		fmt.Printf("Running simulation with size:%d, hills:%d, wrecks:%d, submarine:%d\n", size, hillsNumber, wrecksNumber, submarine)

		pythonScript := exec.Command("python3", "./python/main.py", strconv.Itoa(size), strconv.Itoa(hillsNumber), strconv.Itoa(wrecksNumber), strconv.Itoa(submarine))
		output, err := pythonScript.CombinedOutput()

		if err != nil {
			fmt.Println("Error running python script:", err)
		}

		var data struct {
			Submarines []models.Submarine `json:"submarines"`
			MaxDepth   [][]float64        `json:"seafloor"`
			Dimension  int                `json:"dimension"`
			Wrecks     [][]float64        `json:"wrecks"`
		}

		if err := json.Unmarshal(output, &data); err != nil {
			println("Failed to parse Python output:", string(output))
			log.Fatal("Failed to parse Python output:", err)
		}

		id := db.SaveSimulation(models.Simulation{
			Name:      cmd.Flag("name").Value.String(),
			Dimension: data.Dimension,
		})
		db.SaveSeaFloor(id, data.MaxDepth)
		db.SaveSubmarines(id, data.Submarines)
		db.SaveWrecks(id, data.Wrecks)
	},
}

var simulationHistory = &cobra.Command{
	Use:   "history",
	Short: "Show simulation history",
	Long:  `Show simulation history`,
	Run: func(cmd *cobra.Command, args []string) {
		startDate, _ := cmd.Flags().GetString("start")
		endDate, _ := cmd.Flags().GetString("end")

		startDate = startDate[:10]
		endDate = endDate[:10]

		fmt.Printf("Fetching simulation history from %s to %s\n", startDate, endDate)

		start, err := time.Parse("2006-01-02", startDate)
		if err != nil {
			log.Fatalf("Invalid start date format: %v", err)
		}
		end, err := time.Parse("2006-01-02", endDate)
		if err != nil {
			log.Fatalf("Invalid end date format: %v", err)
		}

		var data []models.Simulation

		data, err = db.GetSimulationsHistory(start, end)
		if err != nil {
			log.Fatal("Failed to retrieve simulation history:", err)
		}

		fmt.Println("Simulation history:")
		for _, sim := range data {
			sim.Date = sim.Date.Local()
			fmt.Printf("ID: %d, Name: %s, Date: %s\n", sim.Id, sim.Name, sim.Date.Format("2006-01-02 15:04:05"))
		}

	},
}

var prediction = &cobra.Command{
	Use:   "predict",
	Short: "Predict submarine path based on simulation data",
	Run: func(cmd *cobra.Command, args []string) {
		simulationID, err := cmd.Flags().GetInt("id")
		if err != nil {
			log.Fatalf("Error retrieving simulation ID: %v", err)
		}

		data, err := db.GetSimulationDetails(simulationID)
		if err != nil {
			log.Fatalf("Error fetching simulation details: %v", err)
		}

		jsonData, err := json.Marshal(data)
		if err != nil {
			log.Fatalf("Error marshaling data: %v", err)
		}

		_ = os.WriteFile("./simulation_data/simulation.json", jsonData, 0644)

		pythonScript := exec.Command(
			"python3",
			"./python/prediction.py",
			"./simulation_data/simulation.json",
		)

		output, err := pythonScript.CombinedOutput()
		if err != nil {
			log.Printf("Error executing Python script: %v", err)
			log.Printf("Python script output: %s", string(output))
			return
		}
	},
}

var heatmap = &cobra.Command{
	Use:   "heatmap",
	Short: "Generate heatmap of probability from simulation data",
	Run: func(cmd *cobra.Command, args []string) {
		simulationID, err := cmd.Flags().GetInt("id")
		if err != nil {
			log.Fatalf("Error retrieving simulation ID: %v", err)
		}

		data, err := db.GetSimulationDetails(simulationID)
		if err != nil {
			log.Fatalf("Error fetching simulation details: %v", err)
		}

		jsonData, err := json.Marshal(data)
		if err != nil {
			log.Fatalf("Error marshaling data: %v", err)
		}

		_ = os.WriteFile("./simulation_data/simulation.json", jsonData, 0644)

		pythonScript := exec.Command(
			"python3",
			"./python/heatmap.py",
			"./simulation_data/simulation.json",
		)

		output, err := pythonScript.CombinedOutput()
		if err != nil {
			log.Printf("Error executing Python script: %v", err)
			log.Printf("Python script output: %s", string(output))
			return
		}
	},
}

var plot = &cobra.Command{
	Use:   "plot",
	Short: "Plot simulation data",
	Run: func(cmd *cobra.Command, args []string) {
		simulationID, err := cmd.Flags().GetInt("id")
		if err != nil {
			log.Fatalf("Error retrieving simulation ID: %v", err)
		}

		data, err := db.GetSimulationDetails(simulationID)
		if err != nil {
			log.Fatalf("Error fetching simulation details: %v", err)
		}

		jsonData, err := json.Marshal(data)
		if err != nil {
			log.Fatalf("Error marshaling data: %v", err)
		}

		_ = os.WriteFile("./simulation_data/simulation.json", jsonData, 0644)

		pythonScript := exec.Command(
			"python3",
			"./python/plot.py",
			"./simulation_data/simulation.json",
		)

		output, err := pythonScript.CombinedOutput()
		if err != nil {
			log.Printf("Error executing Python script: %v", err)
			log.Printf("Python script output: %s", string(output))
			return
		}
	},
}

func init() {
	dateNow := time.Now().Format("2006-01-02_15-04-05")
	dateTomorrow := time.Now().AddDate(0, 0, 1).Format("2006-01-02_15-04-05")
	dateOneWeekAgo := time.Now().AddDate(0, 0, -7).Format("2006-01-02_15-04-05")

	rootCmd.AddCommand(run)
	run.Flags().Int("size", 1000, "Seafloor size")
	run.Flags().Int("hills", 8, "Number of hills")
	run.Flags().Int("wrecks", 8, "Number of wrecks")
	run.Flags().Int("submarine", 3, "Number of submarines")
	run.Flags().String("name", dateNow, "Name of the simulation")

	rootCmd.AddCommand(simulationHistory)
	simulationHistory.Flags().String("start", dateOneWeekAgo, "Start date in format YYYY-MM-DD")
	simulationHistory.Flags().String("end", dateTomorrow, "End date in format YYYY-MM-DD")

	rootCmd.AddCommand(plot)
	plot.Flags().Int("id", 0, "Simulation ID")

	rootCmd.AddCommand(prediction)
	prediction.Flags().Int("id", 0, "Simulation ID")

	rootCmd.AddCommand(heatmap)
	heatmap.Flags().Int("id", 0, "Simulation ID")

}
