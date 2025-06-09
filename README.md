# Oceangate Simulation

## How to run (manually):
- make sure go is installed
- In the working directory execute
```bash
go mod download
go install
```
- Run the example simulation
```bash
oceangate run --size 1000 --hills 7 --wrecks 9 --submarine 4
```

## How to run application with docker:
```bash
docker compose up 
```
This will build the command line interface and database images and run in a containers.

To actually use commands you need to attach to container terminal
```bash
docker exec -it <container_id> /bin/bash
```
Or if you are using windows:
```bash
docker exec -it <container_id> //bin//bash
```
Then you can run the commands as described below.

## Available Commands:
### `run`
Run the submarine simulation and store the data in the database.
```bash
oceangate run --size <int> --hills <int> --wrecks <int> --submarine <int> --name <string>
```
- `--size`: Seafloor size (default: 1000)
- `--hills`: Number of hills (default: 8)
- `--wrecks`: Number of wrecks (default: 8)
- `--submarine`: Number of submarines (default: 3)
- `--name`: Name of the simulation (default: current timestamp)

### `history`
Show the simulation history within a date range.
```bash
oceangate history --start <YYYY-MM-DD> --end <YYYY-MM-DD>
```
- `--start`: Start date in format `YYYY-MM-DD` (default: one week ago)
- `--end`: End date in format `YYYY-MM-DD` (default: tomorrow)

### `plot`
Plot simulation data.
```bash
oceangate plot --id <int>
```
- `--id`: Simulation ID (required)

### `predict`
*Not yet implemented*

Predict the submarine path based on simulation data.
```bash
oceangate predict --id <int>
```
- `--id`: Simulation ID (required)

### `heatmap`
*Not yet implemented*

Generate a heatmap of probabilities from simulation data.
```bash
oceangate heatmap --id <int>
```
- `--id`: Simulation ID (required)


## Additional Notes:

Generated visualization using the `run`, `plot` and `heatmap` commands will be stored in visualization directory.
Simulation data that is being fetch from the database will be stored in the `simulation_data` directory.
