@echo off
setlocal enabledelayedexpansion

if "%1"=="start" (
    echo Starting web application...
    docker compose -f docker-compose.dev.yml up -d
    echo Application started at http://localhost:5005
    exit /b 0
)

if "%1"=="start-debug" (
    echo Starting web application...
    docker compose -f docker-compose.dev.yml up -d
    echo Application started at http://localhost:5005
    echo Showing logs...
    docker compose -f docker-compose.dev.yml logs -f
    exit /b 0
)

if "%1"=="stop" (
    echo Stopping web application...
    docker compose -f docker-compose.dev.yml down
    echo Application stopped
    exit /b 0
)

if "%1"=="restart" (
    echo Restarting web application...
    docker compose -f docker-compose.dev.yml down
    docker compose -f docker-compose.dev.yml up -d
    echo Application restarted at http://localhost:5005
    exit /b 0
)

if "%1"=="delete" (
    echo Stopping and removing web application...
    docker compose -f docker-compose.dev.yml down
    docker rmi aimses-web:latest
    echo Application removed
    exit /b 0
)

echo Usage: manage-app.bat [start^|start-debug^|stop^|restart^|delete]
echo   start       - Start the web application
echo   start-debug - Start the web application and show logs
echo   stop        - Stop the web application
echo   restart     - Restart the web application
echo   delete      - Stop and remove the web application
exit /b 1