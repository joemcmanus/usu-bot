#Startup file for the website
#Put file in /lib/systemd/system
#run systemctl enable flask.service 

[Unit]
Description=Flask App for IoT
After=network.target

[Service]
Type=forking
PIDFile=/var/run/flask.pid
WorkingDirectory=/home/aggies/tankbotROS-master/nonROS
ExecStart=/usr/bin/gunicorn --bind 0.0.0.0:80 server:app -p /var/run/flask.pid --daemon
RestartSec=30s
Restart=always
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID

[Install]
WantedBy=multi-user.target
