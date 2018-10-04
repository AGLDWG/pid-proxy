echo "Copying files to /etc/apache2/sites-available/"
sudo cp conf/*.conf /etc/apache2/sites-available/

echo "Restarting apache2"
sudo service apache2 restart
