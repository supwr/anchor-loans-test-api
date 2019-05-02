### Wedding Gallery

This project was developed using docker, python 3 and Ionic PWA(for the frontend).
Flask framework was chosen for the task because of the ease to configure and get a robust application available.
The use of Flask, along with Mongo and JWT, allow the application to scale horizontally with no greater headaches.
The application was deployed to Digital Ocean, using Docker.


### The intention behind the application


>You got a request from a friend to create a gallery for his weeding where his 
>friends will be able to upload their photos and he`ll have a unified gallery with 
>all friend's photos.
>He wants to be able to approve the the photos before be visible to everyone. He 
>and his wife should be the only one able to approve new photos.
>Users must be able to like photos.
>Users should be able to sort the photos by total of likes or by date taken.

>Please create a website that supply their needs. The photos must be saved on  
>Amazon AWS S3 and the gallery must be fast to open even if there many photos.

### Running the application

Inside the root folder, clone the frontend code, in order to have all the containers with their respective codes:

```git clone https://github.com/supwr/anchor-loans-test-front.git wedding-gallery-front```

In order to get the files to the right S3 bucket, you need to change the env variables present in the docker-compose.yml:

```sh
- AWS_ACCESS_KEY_ID=YOUR_AWS_ACCOUNT_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY=YOUR_AWS_ACCOUNT__ACCESS_KEY_ID
```

A Postman collection is present at the root folder, so you can test all the requests.

Then, execute docker-compose to get all the containers up and running:

```docker-compsose up -d --build```

At this point, you should have 3 containers running:
- A MongoDB server;
- A Nginx container serving the frontend;
- A Nginx container serving the backend;



### TODO

- Validation of file types, allowing only images to be uploaded;
- Ordering by likes or date;
- Unit Tests.