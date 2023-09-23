#!/bin/bash

REPO_URL="git@github.com:kenho811/connexion-example.git"
REPO_DIR="connexion-example"

if [ -d "$REPO_DIR" ]; then
  echo "Repository exists. Pulling latest changes..."
  cd "$REPO_DIR"
  git pull
else
  echo "Repository does not exist. Cloning..."
  git clone "$REPO_URL"
fi



# Step 2: Build image if not exists. Check if the image named "connexion-example" already exists
if docker image inspect connexion-example >/dev/null 2>&1; then
  echo "An image named 'connexion-example' already exists. Not doing anything."
else
  docker build -t connexion-example .
fi

# Step 3: Run Container
# Check if port 8080 is in use
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
  echo "Port 8080 is already in use. Please free up the port and try again."
  exit 1
fi

# Check if a container with the name "connexion-example" already exists and force remove it
if docker ps -a --format '{{.Names}}' | grep -q "connexion-example"; then
  docker rm -f connexion-example
fi

# Run the docker run command with container name set to "connexion-example"
docker run -d -p 8080:8080 --name connexion-example connexion-example
echo 'please check http://localhost:8080/ui'
