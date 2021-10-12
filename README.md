# Django Real-Time Chatroom
Repository for developing a real-time chatroom using Django Channels web socket and Redis. This side-project serves as a prototype/proof-of-concept for developing a real-time chatroom for mental health experts to communicate with Arduino smart watch users as part of my Final Year Project (FYP) titled 'Fitweet: Arduino-based Smart Watch for Early Anticipatory Anxiety Notification System'.

![alt](https://im.ezgif.com/tmp/ezgif-1-2b3591833279.gif)

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
