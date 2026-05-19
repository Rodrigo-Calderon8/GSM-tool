#!/bin/bash

# Start the containers
docker compose up -d

# Give it a moment to start
sleep 3

# Try to open the browser automatically
case "$OSTYPE" in
  linux*)       xdg-open http://localhost:3000 ;;
  darwin*)      open http://localhost:3000 ;;
  msys*|cygwin*) start http://localhost:3000 ;;
  *)            echo "Please open http://localhost:3000 in your browser." ;;
esac
