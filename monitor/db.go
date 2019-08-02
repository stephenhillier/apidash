package main

import (
	"log"
	"time"

	"github.com/jmoiron/sqlx"

	// register postgres driver
	"github.com/lib/pq"
)

// Datastore represents a database with an open connection
type Datastore struct {
	*sqlx.DB
}

// NewDatastore takes a sqlx.DB handle and returns a
// Datastore. It blocks until the DB is ready.
func NewDatastore(db *sqlx.DB) (*Datastore, error) {
	for {
		var x int
		err := db.Get(&x, "SELECT 1")
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
	pq.NullTime
}
