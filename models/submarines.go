package models

type Point struct {
	X    float64 `json:"x"`
	Y    float64 `json:"y"`
	Z    float64 `json:"z"`
	Prob float64 `json:"prob"`
}

type Submarine struct {
	ID   int     `json:"id"`
	Path []Point `json:"path"`
}
