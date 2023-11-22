# Makefile

# Define the Docker image name
IMAGE_NAME=gif-search-app

# Define the port number to be exposed
PORT=8080

.PHONY: build run stop clean

# Builds, runs test and runs the Docker Image
start:
	@echo "Building the Docker image..."
	docker build -t $(IMAGE_NAME) .

	@echo "Running unit tests..."
	docker run --rm $(IMAGE_NAME) python test_app.py

	@echo "Running the Docker container..."
	docker run --env-file .env -p $(PORT):$(PORT) $(IMAGE_NAME)

# Clean up the Docker image and container
clean: stop
	@echo "Removing the Docker image..."
	docker rmi $(IMAGE_NAME)
