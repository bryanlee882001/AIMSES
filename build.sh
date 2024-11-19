#!/bin/bash
set -e

BUILD_MODE=$1
PROJECT_NAME=aimses-web-application

# Detect platform
if [[ $(uname -m) == "arm64" ]]; then
    PLATFORM="linux/arm64/v8"
else
    PLATFORM="linux/amd64"
fi

build_initial() {
    echo "Building application image..."
    echo "Platform: $PLATFORM"

    docker-compose -f docker-compose.build.yml down
    docker rmi $PROJECT_NAME-web:latest 2>/dev/null || true

    export DOCKER_PLATFORM=$PLATFORM
    docker-compose -f docker-compose.build.yml --build --no-cache

    echo "Image built successfully!"
}

build_data() {
    echo "Creating distribution package..."
    mkdir -p dist/db
    
    echo "Saving web image..."
    docker save $PROJECT_NAME-web:latest -o dist/aimses-web.tar
    
    # Copy files
    cp docker-compose.prod.yml dist/docker-compose.yml
    cp README.md dist/
    cp start-app.sh dist/
    cp start-app.bat dist/
    
    # Copy database
    cp db/database.db dist/db/
    
    echo "Creating distribution archive..."
    tar -czf aimses-distribution.tar.gz -C dist .
    
    echo "Generating SHA256 hash..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        shasum -a 256 aimses-distribution.tar.gz > aimses-distribution.tar.gz.sha256
    else
        sha256sum aimses-distribution.tar.gz > aimses-distribution.tar.gz.sha256
    fi
    
    echo "Cleaning up..."
    rm -rf dist

    echo "Distribution package created successfully!"
}

case "$BUILD_MODE" in
    "init")
        build_initial
        ;;
    "export")
        build_data
        ;;
    *)
        echo "Usage: ./build.sh [init|data]"
        echo "  init: Build initial application image"
        echo "  data: Create distribution package"
        exit 1
        ;;
esac