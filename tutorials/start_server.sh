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