# 101-setup_web_static.pp

# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Ensure the necessary directories are present
file { ['/data/', '/data/web_static/', '/data/web_static/releases/', '/data/web_static/shared', '/data/web_static/releases/test/']:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create a test HTML file
file ( '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
 <html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

# Create a symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  force  => true,
}

# Ensure ownership of /data/ directory
file { '/data/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Configure Nginx
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \$hostname;
    root   /var/www/html;
    index  index.html index.htm;

   location /hbnb_static {
       alias /data/web_static/current;
       index index.html index.htm;
   }

   location /redirect_me {
       return 301 http://github.com/Dev-Kings;
   }

   error_page 404 /404.html;
   location /404 {
     root /var/www/html;
     internal;
   }
}",
  notify  => Service['nginx'],
}

# Ensure Nginx service is running
service { 'nginx':
  ensure => running,
  enable => true,
}
