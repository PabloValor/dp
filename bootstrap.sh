# General
apt-get update
#apt-get -y upgrade
apt-get install -y build-essential
apt-get install -y make
apt-get install -y curl
apt-get install -y git

# Database
PG_VERSION=9.1
apt-get -y install "postgresql-$PG_VERSION" "postgresql-contrib-$PG_VERSION"

APP_DB_USER=dp
APP_DB_PASS=dp
APP_DB_NAME=$APP_DB_USER

cat << EOF | su - postgres -c psql
-- Create the database user:
CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS';

-- SUPERUSER
ALTER USER $APP_DB_USER WITH SUPERUSER;

-- Create the database:
CREATE DATABASE $APP_DB_NAME WITH OWNER $APP_DB_USER;

EOF

sed -i  s/peer/md5/ /etc/postgresql/9.1/main/pg_hba.conf
service postgresql restart

# Image 
apt-get -y install imagemagick
apt-get -y install libjpeg-dev

# Redis - https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis
apt-get install tcl8.5
wget http://download.redis.io/releases/redis-2.8.9.tar.gz
tar xzf redis-2.8.9.tar.gz
cd redis-2.8.9
make
make test
make install
cd utils
./install_server.sh
cd 
rm -rf redis-2.8.9
rm redis-2.8.9.tar.gz

# Python dev
apt-get -y install python-dev libpq-dev
apt-get -y install python-pip

# Backend dependencies
pip install virtualenv
cd /vagrant
virtualenv env
source env/bin/activate
pip install -r /vagrant/requirements.txt

echo 'export AWS_ACCESS_KEY_ID=0G8GTV79ZZV2202XW682' >> /home/vagrant/.bashrc
echo "export AWS_SECRET_ACCESS_KEY=0MB3tAjz816yOjxmbMFMU0hTRA4PNNbKW6RkrLRl" >> /home/vagrant/.bashrc
echo 'export MANDRILL_API_KEY=4rbqFI0BJL8ryoHT7CRGLw' >> /home/vagrant/.bashrc
source /home/vagrant/.bashrc

cd /vagrant/web-api
./manage syncdb
./manage migrate
./manage.py loaddata tournaments/fixtures/argentina_2014.json

# Frontend dependencies
curl -sL https://deb.nodesource.com/setup | sudo bash -
apt-get install -y nodejs
npm install -g coffee-script
npm install -g grunt-cli
cd /vagrant/web-frontend
npm install
gem install compass

