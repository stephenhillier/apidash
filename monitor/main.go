package main

import (
	"fmt"
	"log"
	"os"
	"os/signal"
	"time"

	"github.com/go-pg/pg/v9"

	"github.com/namsral/flag"
)

// App is the monitoring app, started with a database to retrieve monitor definitions from
type App struct {
	DB *Datastore
}

func main() {
	var dbuser, dbpass, dbname, dbhost, dbport, dbsslmode string
	flag.StringVar(&dbuser, "POSTGRES_USER", "dash", "database username")
	flag.StringVar(&dbpass, "POSTGRES_PASSWORD", "", "database password")
	flag.StringVar(&dbname, "POSTGRES_DB", "dash", "database name")
	flag.StringVar(&dbhost, "POSTGRES_SERVER", "db", "database service host")
	flag.StringVar(&dbport, "dbport", "5432", "database service port")
	flag.StringVar(&dbsslmode, "dbsslmode", "disable", "database ssl mode")
	flag.Parse()

	db := pg.Connect(&pg.Options{
		Addr:     fmt.Sprintf("%s:%s", dbhost, dbport),
		User:     dbuser,
		Password: dbpass,
		Database: dbname,
	})
	defer db.Close()

	datastore, err := NewDatastore(db)
	if err != nil {
		log.Panic("Could not connect to database")
	}

	app := &App{
		DB: datastore,
	}

	log.Println("Starting to run monitors...")
	go app.monitor()

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt)

	// App running; Wait here for interrupt signal...
	<-stop
	log.Println("Shutting down...")
	log.Println("Application shut down.")
}

func (app *App) monitor() {
	var monitors []*Monitor
	var err error
	var results []result
	for {
		time.Sleep(5 * time.Second)
		monitors, err = app.DB.getMonitors()
		if err != nil {
			log.Println(err)
		}
		if len(monitors) == 0 {
			continue
		}
		results = makeRequests(monitors, 5)
		log.Println(results)
		break
	}
}
