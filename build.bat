@echo off
setlocal enabledelayedexpansion

set BUILD_MODE=%1
set PROJECT_NAME=aimses-web-application

REM Detect platform
wmic os get osarchitecture | find "ARM" > nul
if not errorlevel 1 (
    set PLATFORM=linux/arm64/v8
) else (
    set PLATFORM=linux/amd64
)

if "%BUILD_MODE%"=="init" goto build_initial
if "%BUILD_MODE%"=="export" goto build_data
echo Usage: build.bat [init^|data]
echo   init: Build initial application image
echo   data: Create distribution package
exit /b 1

:build_initial
echo Building application image...
echo Platform: %PLATFORM%

docker compose -f docker-compose.build.yml down
docker rmi %PROJECT_NAME%-web:latest 2>nul || exit /b 0

set DOCKER_PLATFORM=%PLATFORM%
docker compose -f docker-compose.dev.yml build --no-cache

echo Image built successfully! Access the website through localhost: 127.0.0.1:5005
exit /b 0

:build_data
echo Creating distribution package...
if not exist dist mkdir dist
if not exist dist\db mkdir dist\db

echo Saving web image...
docker save %PROJECT_NAME%-web:latest -o dist\aimses-web.tar

REM Copy files
copy docker-compose.prod.yml dist\docker-compose.yml
copy README.md dist\
copy start-app.sh dist\
copy start-app.bat dist\

REM Copy database to separate folder
copy db\database.db dist\db\

echo Creating distribution archive...
cd dist
tar -czf ..\aimses-distribution.tar.gz *
cd ..

echo Generating SHA256 hash...
certutil -hashfile aimses-distribution.tar.gz SHA256 > aimses-distribution.tar.gz.sha256

echo Cleaning up...
rmdir /s /q dist

echo Distribution package created successfully!
exit /b 0