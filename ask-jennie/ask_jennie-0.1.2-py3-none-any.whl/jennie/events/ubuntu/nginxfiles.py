NGINX_PORT_CONF = '''server {
        listen PORT;

        index index.html index.htm index.nginx-debian.html index.php;
        server_name DOMAIN;

        location / {
            root ROOT;
            try_files $uri $uri/ =404;
        }

}'''

NGINX_HTTP_CONF = '''server {
        listen 80;

        index index.html index.htm index.nginx-debian.html index.php;
        server_name DOMAIN;

        location / {
            root ROOT;
            try_files $uri $uri/ =404;
        }

}'''

NGINX_HTTPS_CONF = '''server {
        listen 443;

        index index.html index.htm index.nginx-debian.html index.php;
        server_name DOMAIN;

        ssl on;
        ssl_certificate  /etc/letsencrypt/live/DOMAIN_NAME/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/DOMAIN_NAME/privkey.pem;

        location / {
            root ROOT;
            try_files $uri $uri/ =404;
        }

}'''

DEFAULT_CONF = '''server {
        listen 80;
        root /var/www/html;
        index index.html index.htm index.nginx-debian.html index.php;
        server_name localhost;

        location / {
            try_files $uri $uri/ =404;
        }

        location ~ \.php$ {
            include snippets/fastcgi-php.conf;
            fastcgi_pass unix:/var/run/php/php7.2-fpm.sock;
        }

}'''

DEFAULT_PHPMYADMIN_CONF = '''server {
        listen 80;
        root /var/www/html;
        index index.php index.html index.htm index.nginx-debian.html;
        server_name localhost;

        location / {
            try_files $uri $uri/ =404;
        }

        location ~ \.php$ {
            include snippets/fastcgi-php.conf;
            fastcgi_pass unix:/var/run/php/php7.2-fpm.sock;
        }

}'''

KIBANA_CONF = '''server {
    listen 8100;

    server_name kibana;

    location / {
        proxy_pass http://localhost:5601;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}'''

DJANGO_HTTPS_CONF = '''upstream backend {
    server 127.0.0.1:PORT_EXCHANGE;      # for a web port socket
}

server {
        listen 443;
        listen [::]:443;

        server_name DOMAIN_NAME;
        ssl on;
        ssl_certificate  /etc/letsencrypt/live/DOMAIN_NAME/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/DOMAIN_NAME/privkey.pem;

        charset     utf-8;

        #Max upload size
        client_max_body_size 75M;   # adjust to taste

        # Finally, send all non-media requests to the Django server.
        location / {
                uwsgi_pass  backend;
                include     /etc/nginx/uwsgi_params;
        }
}'''

DJANGO_HTTP_CONF = '''upstream backend {
    server 127.0.0.1:PORT_EXCHANGE;      # for a web port socket
}

server {
        listen 80;
        listen [::]:80;

        server_name DOMAIN_NAME;

        charset     utf-8;

        #Max upload size
        client_max_body_size 75M;   # adjust to taste

        # Finally, send all non-media requests to the Django server.
        location / {
                uwsgi_pass  backend;
                include     /etc/nginx/uwsgi_params;
        }
}'''

DJANGO_PORT_CONF = '''upstream backend {
    server 127.0.0.1:PORT_EXCHANGE;      # for a web port socket
}

server {
        listen PORT;
        listen [::]:PORT;

        server_name DOMAIN_NAME;

        charset     utf-8;

        #Max upload size
        client_max_body_size 75M;   # adjust to taste

        # Finally, send all non-media requests to the Django server.
        location / {
                uwsgi_pass  backend;
                include     /etc/nginx/uwsgi_params;
        }
}'''

DEFAULT_PHP_PAGE = '''<?php

// Show all information, defaults to INFO_ALL
phpinfo();

?>
'''