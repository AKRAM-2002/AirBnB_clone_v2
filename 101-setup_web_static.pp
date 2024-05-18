# web_server_setup.pp

# Ensure Nginx is installed and up to date
package { 'nginx':
  ensure => 'latest',
}

# Ensure nginx service is running and enabled
service { 'nginx':
  ensure => 'running',
  enable => true,
  require => Package['nginx'],
}

# Create directory structure
file { ['/data/web_static/releases/test', '/data/web_static/shared']:
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create index.html file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => 'Holberton School',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test/',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static/releases/test/index.html'],
}

# Add location block to Nginx configuration
file_line { 'add_hbnb_static_location':
  path    => '/etc/nginx/sites-available/default',
  line    => '    location /hbnb_static/ {',
  before  => '    }',
  require => Package['nginx'],
}

file_line { 'add_hbnb_static_alias':
  path    => '/etc/nginx/sites-available/default',
  line    => '        alias /data/web_static/current/;',
  before  => '    }',
  require => Package['nginx'],
}

# Restart Nginx to apply changes
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => [
    Package['nginx'],
    File['add_hbnb_static_location'],
    File['add_hbnb_static_alias'],
  ],
}
