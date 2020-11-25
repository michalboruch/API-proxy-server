PROJECT_APP_NAME=een-api-simple-proxy

build:
	docker build -t ${PROJECT_APP_NAME}:latest -f Dockerfile .

run:
	docker run -v $(shell pwd):/usr/src/app -it ${PROJECT_APP_NAME}
