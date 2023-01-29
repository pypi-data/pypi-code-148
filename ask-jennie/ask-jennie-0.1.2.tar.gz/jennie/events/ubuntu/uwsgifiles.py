UWSGI_EMPEROR_SERVICE = '''[Unit]
Description=uwsgi service

[Service]
User=root
WorkingDirectory=/usr/local/bin
ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi

[Install]
WantedBy=multi-user.target'''


DJANGO_CONF = '''[uwsgi]
project = PROJECT_DIR

chdir = MAIN_DIR
module = %(project).wsgi:application

master = true
processes = 1
socket = 127.0.0.1:PORT_EXCHANGE
chmod-socket = 664
vacum = true
daemonize = /var/log/server_PORT_EXCHANGE.log
py-autoreload = 1'''