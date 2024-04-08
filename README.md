# eNtweniChatBackend

## Description

This project implements a real-time chat application, allowing users to connect, exchange messages, and potentially navigate between different screens (depending on the project's scope). It leverages core components like configuration management, navigation management, server communication, and message handling. The backend leverages FastAPI and websockets for efficient communication and utilizes a SQLite database for user and message management.

## `DEPLOY`

Deploying with nginx server
create a conf file -> entwenichat.conf

```conf
server {
    listen 8000;  # Change to desired port if needed
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:8001;  # Adjust port if different
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_buffering on;

        ; For websocket configuaration to be hosted as well
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_http_version 1.1;  # Required for WebSockets
    }
}

```

Then move the conf to sites available, restart the server and test

```sh
sudo ln -s /etc/nginx/sites-available/entweni_chat.conf /etc/nginx/sites-enabled/
    sudo systemctl restart nginx
sudo nginx -t  # Test configuration syntax

sudo systemctl reload nginx  # Reload Nginx if test is successfull

uvicorn main:app --host 0.0.0.0 --port 8001  # Adjust port if needed
```
