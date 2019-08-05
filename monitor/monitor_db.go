package main

import (
	"log"
	"time"
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

func (repo *Datastore) getMonitors() ([]*Monitor, error) {
	query := `
	SELECT
	monitor.id, monitor.name, monitor.endpoint,
	MAX(ck.check_time) as last_checked
	FROM monitor
	LEFT JOIN check_status AS ck ON ck.monitor_id = monitor.id
	GROUP BY monitor.id HAVING coalesce(MAX(ck.check_time) < date_trunc('minute', now()) - interval '4m', true) = true
	LIMIT 5
	`

	monitors := []*Monitor{}

	_, err := repo.Query(&monitors, query)
	log.Printf("Found %v monitors needing a new test", len(monitors))
	return monitors, err
}
