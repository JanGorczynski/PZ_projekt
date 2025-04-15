# Oceangate Simulation

## How to run:
- make sure go is installed
- In the working directory execute
```bash
go mod download
go install
```
- Run the simulation
```bash
oceangate run --size 1000 --hills 7 --wrecks 9 --submarine 4
```
## How to build docker image and run docker container
```bash
docker build -t oceangate .
docker run -e SIZE=1000 -e HILLS=5 -e WRECKS=8 -e SUBMARINE=1 -v ./:/app/ oceangate
```
or
```bash
docker run oceangate -v ./:/app/ 
```
## Run app by docker-compose
```bash
docker compose up
```
