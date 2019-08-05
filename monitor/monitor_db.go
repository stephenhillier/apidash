package main

import (
	"log"
	"time"

	"github.com/go-pg/pg/v9"
)

// Monitor represents an endpoint that is regularly checked
type Monitor struct {
	ID          int64     `sql:"id"`
	Name        string    `sql:"name"`
	Endpoint    string    `sql:"endpoint"`
	CreateTime  time.Time `sql:"create_time"`
	ExpireTime  NullDate  `sql:"expire_time"`
	LastChecked NullDate  `sql:"last_checked"`
}

// checkMonitors opens a transaction and then
// tries to get a lock on the first 5 monitors
// that need to be updated.
func (repo *Datastore) checkMonitors() ([]*Monitor, error) {
	tx, err := repo.Begin()
	if err != nil {
		return nil, err
	}
	// Rollback tx on error.
	defer tx.Rollback()

	query := `
		SELECT monitor.id, monitor.name, monitor.endpoint FROM monitor
		INNER JOIN check_required AS ck ON ck.id = monitor.id
		LIMIT 5
		FOR UPDATE OF monitor SKIP LOCKED
	`

	monitors := []*Monitor{}

	_, err = tx.Query(&monitors, query)

	if err != nil || len(monitors) == 0 {
		tx.Rollback()
		return monitors, err
	}

	log.Printf("Found %v monitors needing a new test", len(monitors))

	results := makeRequests(monitors, 5)
	err = storeResults(tx, results)

	if err != nil {
		tx.Rollback()
		return monitors, err
	}

	tx.Commit()

	return monitors, err
}

func storeResults(tx *pg.Tx, results []*result) error {
	_, err := tx.Model(&results).Insert()
	if err != nil {
		log.Println(err)
	}
	return err
}
