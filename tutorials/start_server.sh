#!/bin/bash

# Step 1: Download Repository
REPO_URL="git@github.com:kenho811/connexion-example.git"
REPO_DIR="connexion-example"

# Check if the repository directory exists
if [ -d "$REPO_DIR" ]; then
  # Directory exists, pull the latest commit
  echo "Repository directory already exists. Pulling latest commit..."
  cd "$REPO_DIR" || exit
  git pull
else
  # Directory does not exist, clone the repository
  echo "Repository directory does not exist. Cloning repository..."
  git clone "$REPO_URL"
  cd clone "$REPO_URL"
fi


# Step 2: Run Docker Container
CONTAINER_NAME="connexion-example"

# Check if the container is already running
if docker ps -a --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
  echo "Container $CONTAINER_NAME exists. Removing the container..."
  docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1
fi

# Build and run the container
docker build -t connexion-example . && docker run -d -p 8080:8080 --name "$CONTAINER_NAME" connexion-example || exit