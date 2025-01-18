# Auroral Ionospheric Magnetospheric Statistical Electron Spectra (AIMSES) Web Application

A web application that computes spectral statistics from data obtained from the NASA's Fast Auroral SnapshoT Explorer (FAST) satellite
based on geographical, ionospheric, and magnetospheric criteria

## System Requirements

- Docker Desktop
- 4GB RAM minimum
- 100GB available disk space (30GB for file and 70GB for Docker Image)
- Operating System:
  1. Linux (x86_64 or ARM64)
  2. Windows 10/11 (x86_64 or ARM64)
  3. macOS (x86_64 or ARM64)

## Installation Steps

### Windows Installation:

1. Extract the Application Files

   - Extract the provided ZIP file to a directory of your choice

2. Build the Application (Note: You only have to build it once)

   - Open Command Prompt
   - Navigate to the extracted directory:
     > cd path\to\extracted\folder
   - Run the build script:
     > .\build.bat init
   - Wait for the build process to complete

3. Start the Application
   - In the same Command Prompt, run:
     > .\manage-app.bat start
   - The application will be available at http://localhost:5005

### Mac Installation:

1. Extract the Application Files

   - Extract the provided ZIP file:
     > unzip application.zip -d destination_folder
   - Navigate to the extracted directory:
     > cd destination_folder

2. Set Execute Permissions

   - Make the scripts executable:
     > chmod +x build.sh manage-app.sh

3. Build the Application (Note: You only have to build it once)

   - Run the build script:
     > ./build.sh init
   - Wait for the build process to complete

4. Start the Application
   - Run:
     > ./manage-app.sh start
   - The application will be available at http://localhost:5005

## Managing the Application

Windows Commands:

```
# Start the application
.\manage-app.bat start

# Stop the application
.\manage-app.bat stop

# Remove the application completely
.\manage-app.bat delete
```

Mac Commands:

```
# Start the application
./manage-app.sh start

# Stop the application
./manage-app.sh stop

# Remove the application completely
./manage-app.sh delete
```

## Troubleshooting

Common Issues:

1. Port Already in Use

   - Error: "port 5005 already allocated"
   - Solution: Stop any application using port 5005 or modify docker-compose.dev.yml to use a different port

2. Docker Not Running

   - Error: "Cannot connect to the Docker daemon"
   - Solution: Start Docker Desktop and wait until it's running (whale icon should be steady)

3. Permission Denied (Mac)

   - Error: "permission denied" when running scripts
   - Solution: Run chmod +x on the scripts again

4. Build Fails

   - Try running with the delete command first, then rebuild:

   Windows:

   ```
   .\manage-app.bat delete
   .\build.bat init
   ```

   Mac:

   ```
   ./manage-app.sh delete
   ./build.sh init
   ```

For Additional Help:

- Check Docker Desktop logs
- Ensure all required files are present in the correct directory structure
- Verify Docker Desktop has adequate resources allocated (Memory, CPU)

## Uninstallation

To completely remove the application:

1. Stop and remove containers:
   Windows:

   > .\manage-app.bat delete

   Mac:

   > ./manage-app.sh delete

2. Delete the application directory


## Notes:
- Error: Chart is not defined at createCharts(): Reference Error