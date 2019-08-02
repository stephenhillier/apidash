package main

import (
	"log"
	"time"

	"github.com/go-pg/pg/v9"
)

// Datastore represents a database with an open connection
type Datastore struct {
	*pg.DB
}

// NewDatastore takes a pg.DB handle and returns a
// Datastore. It blocks until the DB is ready.
func NewDatastore(db *pg.DB) (*Datastore, error) {
	for {
		var x int
		_, err := db.Query(&x, "SELECT 1")
		if err == nil {
			break
		}

		log.Println(err)
		log.Println("Waiting for database to become available")
		time.Sleep(10 * time.Second)
	}
	log.Println("Database connection ready.")
	return &Datastore{db}, nil
}

// NullDate is a nullable date value (for use with PostgreSQL)
type NullDate struct {
	pg.NullTime
}
