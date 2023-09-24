#!/bin/bash

REPO_URL="git@github.com:kenho811/api-server-one.git"
REPO_DIR="api-server-one"

if [ -d "$REPO_DIR" ]; then
  echo "Repository exists. Pulling latest changes..."
  cd "$REPO_DIR"
  git pull
else
  echo "Repository does not exist. Cloning..."
  GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no" git clone "$REPO_URL" "$REPO_DIR"
  cd "$REPO_DIR"
fi


# Step 2: Build image if not exists. Check if the image named "api-server-one" already exists
if docker image inspect api-server-one >/dev/null 2>&1; then
  echo "An image named 'api-server-one' already exists. Not doing anything."
else
  docker build -t api-server-one .
fi

# Step 3: Run Container
# Check if port 8080 is in use
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
  echo "Port 8080 is already in use. Please free up the port and try again."
  exit 1
fi

# Check if a container with the name "api-server-one" already exists and force remove it
if docker ps -a --format '{{.Names}}' | grep -q "api-server-one"; then
  docker rm -f api-server-one
fi

# Run the docker run command with container name set to "api-server-one"
docker run -d -p 8080:8080 --name api-server-one api-server-one
echo 'please check http://localhost:8080/ui'
