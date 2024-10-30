build:
	cp .env ./dags/src/.env
	docker build . --tag extending_airflow:latest
	docker build . --tag streamlit:latest -f Dockerfile.streamlit

run:
	docker run -p 8080:8080 extending_airflow:latest

push:
	docker push extending_airflow:latest

clean:
	docker rmi $(docker images -q)
