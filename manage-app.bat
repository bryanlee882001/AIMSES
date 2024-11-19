@echo off
setlocal enabledelayedexpansion

if "%1"=="start" (
    echo Starting web application...
    docker-compose -f docker-compose.dev.yml up -d
    echo Application started at http://localhost:5005
    exit /b 0
)

if "%1"=="stop" (
    echo Stopping web application...
    docker-compose -f docker-compose.dev.yml down
    echo Application stopped
    exit /b 0
)

if "%1"=="delete" (
    echo Stopping and removing web application...
    docker-compose -f docker-compose.dev.yml down
    docker rmi aimses-web:latest
    echo Application removed
    exit /b 0
)

echo Usage: manage-app.bat [start^|stop^|delete]
echo   start   - Start the web application
echo   stop    - Stop the web application
echo   delete  - Stop and remove the web application
exit /b 1