#!/bin/bash
apt update
apt install -y apache2
echo "Hello from AutoScaled VM" > /var/www/html/index.html
systemctl restart apache2