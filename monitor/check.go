package main

import (
	"log"
	"net/http"
)

type result struct {
	index      int
	statusCode int
	err        error
}

func makeRequests(monitors []*Monitor, limit int) []result {
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
			result := &result{i, res.StatusCode, err}
			resultsChan <- result

			// remove one from semChan
			<-semChan
		}(i, mon)
	}

	var results []result

	for {
		result := <-resultsChan
		results = append(results, *result)

		if len(results) == len(monitors) {
			break
		}
	}

	return results
}
