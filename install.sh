#
# installation file for the PID Proxy Virtual Machine
#
# VM is running Ubuntu 18.04

# update machine, set time
sudo apt update
sudo apt -y upgrade
sudo timedatectl set-timezone Australia/Brisbane

# install Apache server
sudo apt install -y apache2

# install the Apache modules required for redirecting and proxying
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_html
sudo a2enmod xml2enc
sudo a2enmod proxy_ajp
sudo a2enmod filter
sudo a2enmod headers
sudo a2enmod rewrite

# create Apache log files per subdomain
sudo mkdir /var/log/apache2/linked.data.gov.au
sudo touch /var/log/apache2/linked.data.gov.au/access.log
sudo touch /var/log/apache2/linked.data.gov.au/error.log

sudo mkdir /var/log/apache2/environment.data.gov.au
sudo touch /var/log/apache2/environment.data.gov.au/access.log
sudo touch /var/log/apache2/environment.data.gov.au/error.log

sudo mkdir /var/log/apache2/reference.data.gov.au
sudo touch /var/log/apache2/reference.data.gov.au/access.log
sudo touch /var/log/apache2/reference.data.gov.au/error.log

sudo service apache2 restart

# install Git
sudo apt install -y git

# pull the master repo for Apache conf files
git clone https://github.com/AGLDWG/pid-proxy.git /home/ubuntu/backup
