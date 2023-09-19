#!/bin/bash

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
fi