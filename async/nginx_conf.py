http {
  server {
    listen 80;
    client_max_body_size 4G;

    server_name spaceclock.sytes.net;

    location / {
      proxy_set_header Host $http_host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection $connection_upgrade;
      proxy_redirect off;
      proxy_buffering off;
      proxy_pass http://localhost:5000;
    }

    #location /static {
    #  # path for static files
    #  root /path/to/app/static;
    #}
  }

  map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
  }

  upstream uvicorn {
    server unix:/tmp/uvicorn.sock;
  }

}

