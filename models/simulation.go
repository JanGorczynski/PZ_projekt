package models

import "time"

type Simulation struct {
	Id        int
	Name      string
	Date      time.Time
	Dimension int
}
