PROJECT_APP_NAME=een-api-simple-proxy

build:
	docker build -t ${PROJECT_APP_NAME}:latest -f Dockerfile .

run:
	docker run -v $(shell pwd):/usr/src/app -it -p 0.0.0.0:8000:8001 ${PROJECT_APP_NAME}
