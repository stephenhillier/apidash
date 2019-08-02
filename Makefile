loaddata:
	docker-compose exec -T backend /bin/bash -c "python app/initial_data.py"

psql:
	docker-compose exec db /bin/bash -c "psql -U dash -d dash"
