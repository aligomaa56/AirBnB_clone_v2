#!/usr/bin/env bash
#sets up web servers for the deployment of web_static
# Update package lists and install Nginx
apt-get -y update
apt-get -y install nginx

# Prepare directory structure for web server
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

# Create a simple index.html file for testing
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Set up symbolic link to current release
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership of web server directories
chown -R ubuntu:ubuntu /data/

# Configure Nginx to serve static files
sed -i "61i\ \n\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t\tautoindex off;\n\t}" /etc/nginx/sites-available/default

# Restart Nginx to apply changes
service nginx restart
