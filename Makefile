build:
	docker build . --tag extending_airflow:latest

run:
	docker run -p 8080:8080 extending_airflow:latest

push:
	docker push extending_airflow:latest

clean:
	docker rmi $(docker images -q)
	