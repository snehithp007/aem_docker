# aem_docker
 Docker setup for use and throw AEM installation without repository persistence. Best used for local development.

 Instructions:

 1. Run Docker with following specification: 30GB Disk, CPUs: 4, Memory: 8GB, Swap: 4GB
 2. Clone this git repository in your local
 3. Unzip the repository and goto that folder
 4. Place AEM jar in that folder and Rename the jar to following cq-quickstart-6.3.0.jar. If you would like you use current jar name, Dockerfile and aem_installer.py should be updated with the same.
 5. Place license.properties in the same folder
 6. Run following command to build Docker image: ```docker build -t aem -f Dockerfile```.
 7. Run following command to check and build if service's Dockerfile or if repository is updated: ```docker-compose build```
 8. Run following command to start the docker container: ```docker-compose up```


 Few things to consider:
 1. docker-compose.yaml has volume mounted for externalizing the repository. This allows sharing the repository with another docker container (Another AEM instance in our case) if needed. However, this volume is still in docker's VM and needs extra processing if you would like to access it on your machine
 2. docker-compose.yaml has log entry to allow easy access of logs in your machine without having to logging into docker container
 3. Similar setup can be done for publisher and dispatcher installation as well

 Few helpful docker commands:

 To get list of docker images: ```docker images -a```
 -a flag to to get ID of the images

 To delete a specific image:
 ```docker rmi <Image ID>```

 To delete all images:
 ```docker rmi $(docker images -q)```

 To get list of docker containers:
 ```docker container ls -a```

 To remove container
 ```docker container rm <Container ID>```

 To remove all stopped containers
 ```docker container prune```
