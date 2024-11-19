#!/bin/bash

case "$1" in
    "start")
        echo "Starting web application..."
        docker-compose -f docker-compose.dev.yml up -d
        echo "Application started at http://localhost:5005"
        ;;
    "stop")
        echo "Stopping web application..."
        docker-compose -f docker-compose.dev.yml down
        echo "Application stopped"
        ;;
    "delete")
        echo "Stopping and removing web application..."
        docker-compose -f docker-compose.dev.yml down
        docker rmi aimses-web:latest
        echo "Application removed"
        ;;
    *)
        echo "Usage: ./manage-app.sh [start|stop|delete]"
        echo "  start   - Start the web application"
        echo "  stop    - Stop the web application"
        echo "  delete  - Stop and remove the web application"
        exit 1
        ;;
esac
