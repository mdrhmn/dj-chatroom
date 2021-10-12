# Django Real-Time Chatroom
Repository for developing a real-time chatroom using Django Channels web socket and Redis. This side-project serves as a prototype/proof-of-concept for developing a real-time chatroom for mental health experts to communicate with Arduino smart watch users as part of my Final Year Project (FYP) titled 'Fitweet: Arduino-based Smart Watch for Early Anticipatory Anxiety Notification System'.

![alt](https://imgur.com/wMgh8bJ.gif)

## Run Project Locally

To run this app in your local environment, run the following preferably in a virtual environment:

```
pip install -r requirements.txt
```

The app can now be viewed at `localhost:8000` or preferably `127.0.0.1`.

## Running Redis on Docker

Redis is used as a backing store for Channels. Like an in-memory cache. I'm going to use Docker to install and run a Redis server.

If you don't have Docker installed on your computer, you need to install it before you can continue. When you have Docker running, you can run this command to start the redis server:

`docker run -p 6379:6379 -d redis:5`

## Building a Docker Image

To build a Docker image of this application and run it, do the following:

1. Install Docker
2. Build the image using the following:
   ```
   docker build -t <NAME> .
   ```
   - The t flag indicates the name for this image (an optional tag is also possible using the name:tag syntax)
   - The . at the end refers that the Dockerfile is in the current directory (ensure that the image is built when in this project directory)
3. Run the built image using the following:
   ```
   docker run -p 8501:8501 <NAME>
   ```
   - The p flag indicates publishing the exposed port to the host interface.
   - 8501:8501 refers to the binding of the host port to the exposed container port.
   - With this, once the container has started, the application can be viewed at `localhost:8501`.


## WebSockets 101

Normally, Django uses HTTP to communicate between the client and server:

1. The client sends an HTTP request to the server.
2. Django parses the request, extracts a URL, and then matches it to a view.
3. The view processes the request and returns an HTTP response to the client.

Unlike HTTP, the WebSockets protocol allows bi-directional communication, meaning that the server can push data to the client without being prompted by the user. With HTTP, only the client that made a request receives a response. With WebSockets, the server can communicate with multiple clients simultaneously. 

The following shows the architecture of WebSockets using Django Channels:


![alt](https://heroku-www-files.s3.amazonaws.com/django-channels/django-wsgi.png)

## References

1. [Django Realtime Chat App Tutorial - Simple Django Tutorial With Channels And Redis](https://codewithstein.com/django-realtime-chat-app-tutorial-simple-django-tutorial-with-channels-and-redis/)
   - This extensive guide serves as the foundation for this project, where I cloned the repository provided via [this GitHub link](https://github.com/SteinOveHelset/chatty)
   - However, several important modifications were made, particularly in the model and front-end design.
2. [Deploying - Channels 3.0.3 Documentation](https://channels.readthedocs.io/en/latest/deploying.html#)
   - The official documentation of Django Channels is used for future reference on deployment using NGINX, Redis and Daphne.
3. [Deploy Django + Channels + Redis + Heroku + Daphne](https://www.youtube.com/watch?v=zizzeE4Obc0)
   - This YouTube tutorial together with its [GitHub repository](https://github.com/veryacademy/YT-Django-Heroku-Deploy-Channels-Daphne) provides a guide on how to deploy a Django-Channels-Redis-Daphne project on Heroku.
4. [Deploying Docker on Heroku](https://www.youtube.com/watch?v=tTwGdUTR5h8)
    - This YouTube tutorial guides on how to deploy a Docker containers in Heroku, should you decide to deploy it in that manner.