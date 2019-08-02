package main

import (
	"log"
	"net/http"
	"time"
)

type result struct {
	index      int
	tableName  struct{} `sql:"check_status"`
	MonitorID  int64    `sql:"monitor_id"`
	StatusCode int      `sql:"status_code"`
	err        error
	CheckTime  time.Time `sql:"check_time"`
}

func makeRequests(monitors []*Monitor, limit int) []*result {
	// using code from https://gist.github.com/montanaflynn/ea4b92ed640f790c4b9cee36046a5383

	semChan := make(chan struct{}, limit)
	resultsChan := make(chan *result)

	defer func() {
		close(semChan)
		close(resultsChan)
	}()

	for i, mon := range monitors {
		if len(mon.Endpoint) == 0 {
			log.Println("A monitor has an invalid endpoint")
			continue
		}
		go func(i int, m *Monitor) {
			// add request to semChan
			// it will block when limit reached.
			semChan <- struct{}{}

			// get result and add it to resultsChan
			res, err := http.Get(m.Endpoint)
			result := &result{
				index:      i,
				MonitorID:  m.ID,
				StatusCode: res.StatusCode,
				err:        err,
				CheckTime:  time.Now().UTC()}
			resultsChan <- result

			// remove one from semChan
			<-semChan
		}(i, mon)
	}

	var results []*result

	for {
		result := <-resultsChan
		results = append(results, result)

		if len(results) == len(monitors) {
			break
		}
	}

	return results
}

func (app *App) storeResults(results []*result) error {
	log.Printf("storing %s results", len(results))
	res, err := app.DB.Model(&results).Insert()
	log.Println(res)
	if err != nil {
		log.Println(err)
	}
	return err
}
