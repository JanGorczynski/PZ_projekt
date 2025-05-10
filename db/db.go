package db

import (
	"database/sql"
	"fmt"
	_ "github.com/lib/pq"
	"log"
	"oceangate/models"
	"time"
)

var initSQL = `
CREATE TABLE IF NOT EXISTS simulations (
  id SERIAL PRIMARY KEY,
  simulation_name VARCHAR(255) NOT NULL,
  sim_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  dimension INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS submarines (
  id SERIAL PRIMARY KEY,
  simulation_id INTEGER NOT NULL,
  submarine_id INTEGER NOT NULL,
  step_number INTEGER NOT NULL,
  x FLOAT NOT NULL,
  y FLOAT NOT NULL,
  z FLOAT NOT NULL,
  prob FLOAT NOT NULL DEFAULT 0.0,
  FOREIGN KEY (simulation_id) REFERENCES simulations(id)
);

CREATE TABLE IF NOT EXISTS sea_floors (
  simulation_id INTEGER NOT NULL,
  x INTEGER NOT NULL,
  y INTEGER NOT NULL,
  height FLOAT NOT NULL,
  PRIMARY KEY (simulation_id, x, y),
  FOREIGN KEY (simulation_id) REFERENCES simulations(id)
);

CREATE TABLE IF NOT EXISTS wrecks (
  id SERIAL PRIMARY KEY,
  simulation_id INTEGER NOT NULL,
  x INTEGER NOT NULL,
  y INTEGER NOT NULL,
  height FLOAT NOT NULL,
  FOREIGN KEY (simulation_id) REFERENCES simulations(id)
);
`

func connect() (*sql.DB, error) {
	dbConnStr := fmt.Sprintf("user=%s password=%s dbname=%s host=%s port=%s sslmode=disable",
		"postgres", "pz4team2", "postgres", "db", "5432")

	db, err := sql.Open("postgres", dbConnStr)
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %v", err)
	}

	// Ensure DB is reachable
	if err := db.Ping(); err != nil {
		return nil, fmt.Errorf("failed to ping database: %v", err)
	}

	// Execute schema initialization
	if _, err := db.Exec(initSQL); err != nil {
		return nil, fmt.Errorf("failed to initialize database schema: %v", err)
	}

	return db, nil
}

func SaveSubmarines(simulationID int, data []models.Submarine) {
	db, err := connect()
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	insertStmt := `INSERT INTO submarines (simulation_id, submarine_id, step_number, x, y, z, prob) VALUES ($1, $2, $3, $4, $5, $6, $7)`

	for _, sub := range data {
		for stepNumber, pt := range sub.Path {
			_, err := db.Exec(insertStmt, simulationID, sub.ID, stepNumber, pt.X, pt.Y, pt.Z, pt.Prob)
			if err != nil {
				log.Printf("Failed to insert data for submarine %d at step %d: %v", sub.ID, stepNumber, err)
			}
		}
	}

	fmt.Println("Submarine data saved to database.")
}

func SaveSimulation(data models.Simulation) int {
	db, err := connect()
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	insertStmt := `INSERT INTO simulations (simulation_name, dimension) VALUES ($1, $2) RETURNING id`
	var simulationID int
	err = db.QueryRow(insertStmt, data.Name, data.Dimension).Scan(&simulationID)
	if err != nil {
		log.Fatalf("Failed to insert simulation: %v", err)
	}

	fmt.Printf("Simulation saved with ID: %d\n", simulationID)
	return simulationID
}

func GetSimulationsHistory(start, end time.Time) ([]models.Simulation, error) {
	db, err := connect()
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	query := `SELECT id, simulation_name, sim_date FROM simulations WHERE sim_date BETWEEN $1 AND $2`
	rows, err := db.Query(query, start, end)
	if err != nil {
		return nil, fmt.Errorf("failed to query simulations: %v", err)
	}
	defer rows.Close()

	var simulations []models.Simulation
	for rows.Next() {
		var sim models.Simulation
		if err := rows.Scan(&sim.Id, &sim.Name, &sim.Date); err != nil {
			return nil, fmt.Errorf("failed to scan row: %v", err)
		}
		simulations = append(simulations, sim)
	}

	return simulations, nil
}

func SaveWrecks(simulationID int, wrecks [][]float64) {
	db, err := connect()
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	insertStmt := `INSERT INTO wrecks (simulation_id, x, y, height) VALUES ($1, $2, $3, $4)`

	for _, wreck := range wrecks {
		_, err := db.Exec(insertStmt, simulationID, wreck[0], wreck[1], wreck[2])
		if err != nil {
			log.Printf("Failed to insert data for wreck: %v", err)
		}
	}

	fmt.Println("Wreck data saved to database.")
}

func SaveSeaFloor(simulationID int, Z [][]float64) {
	db, err := connect()
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	for x, row := range Z {
		for y, height := range row {
			_, _ = db.Exec(`
				INSERT INTO sea_floors (simulation_id, x, y, height)
				VALUES ($1, $2, $3, $4)
				ON CONFLICT (simulation_id, x, y) DO UPDATE SET height = EXCLUDED.height
			`, simulationID, x, y, height)

		}
	}
}

func GetSimulationDetails(simulationID int) (map[string]interface{}, error) {
	db, err := connect()
	if err != nil {
		return nil, fmt.Errorf("failed to connect to database: %v", err)
	}
	defer db.Close()

	// Retrieve simulation metadata
	println("simulationID", simulationID)
	var dimension int
	err = db.QueryRow(`SELECT dimension FROM simulations WHERE id = $1`, simulationID).Scan(&dimension)
	if err != nil {
		return nil, fmt.Errorf("failed to retrieve simulation metadata: %v", err)
	}

	// Retrieve seafloor data
	rows, err := db.Query(`SELECT x, y, height FROM sea_floors WHERE simulation_id = $1`, simulationID)
	if err != nil {
		return nil, fmt.Errorf("failed to retrieve seafloor data: %v", err)
	}
	defer rows.Close()

	seafloor := make([][]float64, dimension)
	for i := range seafloor {
		seafloor[i] = make([]float64, dimension)
	}

	for rows.Next() {
		var x, y int
		var height float64
		if err := rows.Scan(&x, &y, &height); err != nil {
			return nil, fmt.Errorf("failed to scan seafloor row: %v", err)
		}
		seafloor[x][y] = height
	}

	// Retrieve submarine data
	submarineRows, err := db.Query(`SELECT submarine_id, step_number, x, y, z, prob FROM submarines WHERE simulation_id = $1 ORDER BY submarine_id, step_number`, simulationID)
	if err != nil {
		return nil, fmt.Errorf("failed to retrieve submarine data: %v", err)
	}
	defer submarineRows.Close()

	submarinesMap := make(map[int][]map[string]float64)
	for submarineRows.Next() {
		var submarineID, stepNumber int
		var x, y, z, prob float64
		if err := submarineRows.Scan(&submarineID, &stepNumber, &x, &y, &z, &prob); err != nil {
			return nil, fmt.Errorf("failed to scan submarine row: %v", err)
		}
		submarinesMap[submarineID] = append(submarinesMap[submarineID], map[string]float64{"x": x, "y": y, "z": z, "prob": prob})
	}

	submarines := []map[string]interface{}{}
	for id, path := range submarinesMap {
		submarines = append(submarines, map[string]interface{}{
			"id":   id,
			"path": path,
		})
	}

	// Retrieve wreck data
	wreckRows, err := db.Query(`SELECT x, y, height FROM wrecks WHERE simulation_id = $1`, simulationID)
	if err != nil {
		return nil, fmt.Errorf("failed to retrieve wreck data: %v", err)
	}
	defer wreckRows.Close()
	wrecks := [][]float64{}

	for wreckRows.Next() {
		var x, y, height float64
		if err := wreckRows.Scan(&x, &y, &height); err != nil {
			return nil, fmt.Errorf("failed to scan wreck row: %v", err)
		}
		wrecks = append(wrecks, []float64{x, y, height})
	}

	// Build the final JSON structure
	data := map[string]interface{}{
		"submarines": submarines,
		"seafloor":   seafloor,
		"dimension":  dimension,
		"wrecks":     wrecks,
	}

	return data, nil
}
