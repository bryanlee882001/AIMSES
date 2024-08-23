# Auroral Ionospheric Magnetospheric Statistical Electron Spectra (AIMSES)

## Project Description
A web application that computes spectral statistics from data obtained from the NASA's Fast Auroral SnapshoT Explorer (FAST) satellite. 

Provides:
```
Statistics: Mean, +1/-1σ, Median, 25%, 75%
Spectra: Downward, Upward, Mirroring
Normalization: Raw, Energy Flux, Number Flux
```

Sortable by:
```
Location: TIME, MLT, ILAT, ALT
Ionospheric Conditions: SZA, F10.7
Magnetospheric Conditions: EFLUX, NFLUX, CONJUGATE SZA, KP, AE, 
                           DST, SW DRIVING, LCA, MECHANISMS
```

<br/>

## ER Diagram
![AIMSES ER Diagram](https://github.com/bryanlee882001/AIMSES/assets/63344458/68d90a77-51c1-4d54-b87f-e695f073ba27)

<br/>

## Prerequisites and Instructions

1. Install Docker on your Desktop and Log into your Docker Account: [Installation Guide](https://docs.docker.com/get-docker/)

2. Navigate to Your Project Directory: Open your terminal and change directory (cd) to your project folder where your docker-compose.yml file is located.

3. For Mac with M1 Chip Instructions: If you're using a Mac with an M1 chip,
   uncomment line 7 in your 'docker-compose.yml'
   `platform: linux/x86_64`

4. Run the following command to start your project:
   `docker-compose up`

5. Access the Wesbtie: Open a web browser of your choice: http://127.0.0.1:5005/ . This URL should display your website or application running in Docker.

6. Shutting Down Website: First, run 'docker ps' to find the list of running
   containers. Find the container name associated with the web application image and run this command (Assuming that you've named the container aimses-web):
   `docker stop aimses-web`

<br/>

### Pulling Docker Image from Docker Hub:

1. Log in to Docker Hub (If not already logged in)

2. Pull the image from Docker Hub by running this command:
   `docker pull <private for now>:latest`

3. Run Containers Using Pulled image: Once the image is pulled successfully, you can create a container from it using:
   `docker run -d --name aimses-web <private for now>:latest`

4. Access Website using web browser of your choice: http://127.0.0.1:5005/

