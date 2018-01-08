# Make sure the Apt package lists are up to date, so we're downloading
# version that exist
cookbook_file "apt-sources.list" do
    path "/etc/apt/sources.list"
end

execute 'apt-update' do
    command 'apt-get update'
end

execute 'apt-upgrade' do
    command 'apt-get upgrade -y'
end

# Basic packages:
package "wget"
package "ntp"

# Python3 Packages:
package "python3-pip"
package "libpython3-dev"
package "python3-dev"

# PostgresSQL Packages:
package "postgresql"
package "postgresql-server-dev-all"

# Nginx Packages:
package "nginx"

# Django Package:
execute 'pip-django' do
    command "pip3 install Django==1.11"
end

# Gunicorn Package:
execute 'pip-gunicorn' do
    command "pip3 install gunicorn"
end


# Psycopg2 Package:
execute 'pip-psycopg2' do
    command "pip3 install psycopg2"
end

# WSGI Package:
execute 'pip-wsgi' do
    command "pip3 install uwsgi"
end

# Python Image Library Package:
execute 'pip-PIL' do
    command "pip3 install Pillow"
end

# Python Social Auth Django extension:
execute 'pip-social-auth' do
    command "pip3 install python-social-auth[django]"
end

# Configure NTP... why not
cookbook_file "ntp.conf" do
    path "/etc/ntp.conf"
  end

execute 'ntp-restart' do
    command 'service ntp restart'
end

# Set Nginx configuration
cookbook_file "nginx-default" do
    path "/etc/nginx/sites-available/default"
end

# Set coup.service Gunicorn configuration
cookbook_file "coup-service" do
    path "/etc/systemd/system/coup.service"
end

# Set permissions for Gunicorn settings
execute "coup-service-permissions" do
    command "chmod 755 /etc/systemd/system/coup.service"
end

# Restart gunicorn to apply settings
execute "coup-service-reload" do
    command "systemctl daemon-reload"
end

# Restart Services
execute "restart-nginx" do
    command "systemctl restart nginx"
end

execute "restart-coup-service" do
    command "systemctl restart coup.service"
end


# Create Postgresql server and initialize database:
execute 'postgresql-server-setup' do
    command 'echo "CREATE DATABASE projectdb; CREATE USER vagrant; GRANT ALL PRIVILEGES ON DATABASE projectdb TO vagrant;" | sudo -u postgres psql'
end

# Make Django model migrations if necessary
execute 'django-makemigrations' do
    user 'vagrant'
    cwd '/home/vagrant/final_project/'
    command 'python3 ./manage.py makemigrations'
end

# Migrate model changes to database
execute 'django-migrate' do
    user 'vagrant'
    cwd '/home/vagrant/final_project/'
    command 'python3 ./manage.py migrate'
end

# collect-static to service css files outside code directory
# must set static paths in setting.py and nginx-default
execute 'collect-static' do
    cwd '/home/vagrant/final_project/'
    command 'python3 ./manage.py collectstatic --noinput'
end

# Flush current database before sending initial data
execute 'flush' do
    user 'vagrant'
    cwd '/home/vagrant/final_project/'
    command 'python3 ./manage.py flush --noinput'
  end


# Load initial data fixtures
execute 'load-fixtures' do
    user 'vagrant'
    cwd '/home/vagrant/final_project/'
    command 'python3 ./manage.py loaddata coup/fixtures/*'
end










