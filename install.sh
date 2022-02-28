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

sudo mkdir /var/log/apache2/lab.environment.data.gov.au
sudo touch /var/log/apache2/lab.environment.data.gov.au/access.log
sudo touch /var/log/apache2/lab.environment.data.gov.au/error.log

sudo mkdir /var/log/apache2/reference.data.gov.au
sudo touch /var/log/apache2/reference.data.gov.au/access.log
sudo touch /var/log/apache2/reference.data.gov.au/error.log

sudo mkdir /var/log/apache2/test.linked.data.gov.au
sudo touch /var/log/apache2/test.linked.data.gov.au/access.log
sudo touch /var/log/apache2/test.linked.data.gov.au/error.log

# Add log rotation for log files in the subdirectories of /var/log/apache2.
# Ubuntu-specific! Relies on the first line of /etc/logrotate.d/apache2
# specifying the path to the main log files. 
sudo bash -c "sed -e 's+\*.log+*/*.log+' < /etc/logrotate.d/apache2 > /etc/logrotate.d/apache2-pidproxy"

# install Git
# -- probably already done in standard Ubuntu install
sudo apt install -y git

# pull the master repo for Apache conf files
git clone https://github.com/AGLDWG/pid-proxy.git /home/ubuntu/pid-proxy-config

# copy the repo's .conf file to Apache & enable
sudo rm /etc/apache2/sites-available/*.conf
sudo cp /home/ubuntu/pid-proxy-config/conf/*.conf /etc/apache2/sites-available/
sudo a2ensite 0-linked.data.gov.au.conf
sudo a2ensite 0-linked.data.gov.au-le-ssl.conf
sudo a2ensite catalogue.linked.data.gov.au.conf
sudo a2ensite catalogue.linked.data.gov.au-le-ssl.conf
sudo a2ensite environment.data.gov.au.conf
sudo a2ensite infrastructure.data.gov.au.conf
sudo a2ensite lab.environment.data.gov.au.conf
sudo a2ensite linked.data.gov.au-datasets.conf
sudo a2ensite linked.data.gov.au-ontologies.conf
sudo a2ensite linked.data.gov.au-registers.conf
sudo a2ensite linked.data.gov.au-vocabularies.conf
sudo a2ensite reference.data.gov.au.conf
sudo a2ensite test.linked.data.gov.au.conf
sudo a2ensite www.linked.data.gov.au.conf

# enable HTTPS
# -- follow https://certbot.eff.org/instructions?ws=apache&os=ubuntufocal

# implement Apache mappings
sudo service apache2 restart
