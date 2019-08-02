package main

import (
	"log"
	"time"
)

// Monitor represents an endpoint that is regularly checked
type Monitor struct {
	ID          int64     `db:"id"`
	Name        string    `db:"name"`
	Endpoint    string    `db:"endpoint"`
	CreateTime  time.Time `db:"create_time"`
	ExpireTime  NullDate  `db:"expire_time"`
	LastChecked NullDate  `db:"last_checked"`
}

func (repo *Datastore) getMonitors() ([]*Monitor, error) {
	query := `
	SELECT
	monitor.id, monitor.name, monitor.endpoint,
	MAX(ck.check_time) as last_checked
	FROM monitor
	LEFT JOIN check_status AS ck ON ck.monitor_id = monitor.id
	GROUP BY monitor.id HAVING MAX(ck.check_time) < date_trunc('minute', now()) - interval '1m'
	LIMIT 5
	`

	monitors := []*Monitor{}

	err := repo.Select(&monitors, query)
	log.Printf("Found %v monitors needing a new test", len(monitors))
	return monitors, err
}
