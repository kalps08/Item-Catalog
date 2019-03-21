# Linux Server Configuration

# Project Overview
The objective of this project is to have our web application, Item-Catalog run live on a secure web server. We take a baseline installation of a Linux server instance on a virtual machine, using Amazon Lightsail. We prepare it to host our web application by securing it from a number of attack vectors and by installing and configuring a web server and a database server. Finally, we deploy our existing web application on it. 

Link to Project: http://34.220.148.31/
•	Public IP Address: 34.220.148.31
•	Accessible SSH port: 2200

# Steps to configure a secured Linux Server:
# 1. Create Development Environment Instance
•	Set up an Amazon Web Services account and start a new Ubuntu Linux Server Instance on Amazon Lightsail.
•	Used putty to ssh into the instance as ubuntu user.
•	Download private key provided and note down your public IP address.

# 2. Launch VM and access SSH to the instance
•	Move the private key file into the folder ~/.ssh 	(~   home directory)
o	$ mv /(current_private_key_address)/udacity_key.rsa ~/.ssh/

•	Change the key permission so that only owner can read and write
o	$ chmod 600 ~/.ssh/udacity_key.rsa

•	SSH into the instance either using PUTTY and PUTTY Gen or local command line
o	$ ssh -i ~/.ssh/id_rsa username@public_IP_address -p 2200

# 3. Create New User - Grader
•	Add User grader
o	$ sudo adduser grader
•	Give Sudo Access to grader
$ sudo vim /etc/sudoers.d/grader – add this line to the file - grader ALL=(ALL:ALL) ALL

# 4. Configure the key-based authentication for grader user
•	Generate an encryption key on your local machine
Go to the directory where you want to save the key, and run the following command:
$ ssh-keygen -t rsa key_name
•	Place the public key on the server that we want to use:
$ ssh-copy-id grader@XX.XX.XX.XX -i (key_name.pub)
•	Log into remote machine as grader
 $ ssh -i udacity_key.rsa grader@XX.XX.XX.XX 
o	sudo su - grader
o	mkdir .ssh
o	touch .ssh/authorized_keys 
o	sudo chmod 700 .ssh
o	sudo chmod 600 .ssh/authorized_keys 
o	nano .ssh/authorized_keys 
o	Then paste the contents of the public key created on the local machine

# 5. Change the SSH port from 22 to 2220, Enforce key-based authentication & Disable login for root user
o	Open sshd_config file
sudo vim /etc/ssh/sshd_config
o	Change the following in the file:
	Find the Port line and edit it to 2200.
	Find the PasswordAuthentication line and edit it to no.
	Find the PermitRootLogin line and edit it to no.
o	Save the file and run sudo service ssh restart
 
# 6. Configure the Uncomplicated Firewall (UFW)
•	$ sudo ufw default deny incoming
•	$ sudo ufw default allow outgoing
•	$ sudo ufw allow 2200/tcp
•	$ sudo ufw allow www
•	$ sudo ufw allow ntp 
•	$ sudo ufw enable

# 7. Change timezone to UTC and Fix language issues

o	Change the timezone to UTC using following command
           $ sudo timedatectl set-timezone UTC.
o	Fix language issues
$ sudo update-locale LANG=en_US.utf8 LANGUAGE=en_US.utf8 LC_ALL=en_US.utf8

# 8. Update all currently installed packages
•	$ sudo apt-get update.
•	$ sudo apt-get upgrade.

# 9. Install and Configure Apache2, mod-wsgi and Git
 	$ sudo apt-get install apache2 libapache2-mod-wsgi git
Enable mod_wsgi:
$ sudo a2enmod wsgi

# 10. Install and configure PostgreSQL
$sudo apt-get install libpq-dev python-dev
$sudo apt-get install postgresql postgresql-contrib
$sudo su – postgres
$psql
Once in psql command line, do these steps:
CREATE USER catalog WITH PASSWORD 'password';
CREATE DATABASE catalog WITH OWNER catalog;
\c catalog
REVOKE ALL ON SCHEMA public FROM public;
GRANT ALL ON SCHEMA public TO catalog;
\q
exit
Note: In your catalog project you should change database engine to:
engine = create_engine('postgresql://catalog:password@localhost/catalog')

# 11. Install Flask and other dependencies
    $ sudo apt-get install python-pip
    $ sudo pip install Flask
    $ sudo pip install httplib2 oauth2client sqlalchemy psycopg2 sqlalchemy_utils
    $ sudo pip install requests
 
# 12. Cloning & Configuring the Catalog app from Github 
•	Make a catalog named directory in /var/www
$ sudo mkdir /var/www/catalog
•	Change the owner of the directory catalog
$ sudo chown -R grader:grader /var/www/catalog
•	Clone the Item Catalog to the catalog directory:
$ git clone https://github.com/kalps08/Item-Catalog.git
•	Make a item_catalog.wsgi file to serve the application over the mod_wsgi. with content:
$ touch item_catalog.wsgi &&vim item_catalog.wsgi
import sys
sys.stdout = sys.stderr
sys.path.insert(0, "/var/www/catalog/")
from app import app as application
•	Inside app.py, models.py & lotsofitems.py,  database connection is now performed with:
engine = create_engine('postgresql://catalog:password@localhost/catalog')
•	Run the models.py and lotsofitems.py once to setup the database and populate it with test data.
$ python models.py
$ python lotsofitems.py

# 13. Configure Apache Server
Open apache server config file and– add following content:
$ sudo vim /etc/apache2/sites-available/000-default.conf 
 serve catalog app
<VirtualHost *:80>
 ServerName <IP_Address or Domain>
 ServerAdmin <Email>
 DocumentRoot /var/www/catalog
 WSGIDaemonProcess catalog user=grader group=grader
 WSGIScriptAlias / /var/www/catalog/catalog.wsgi
 <Directory /var/www/catalog>
    WSGIProcessGroup catalog
    WSGIApplicationGroup %{GLOBAL}
    Require all granted
 </Directory>
 ErrorLog ${APACHE_LOG_DIR}/error.log
 LogLevel warn
 CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
 
# 14. Restart Apache to launch the app
        $sudo service apache2 restart

# Resources & References:
•	Amazon EC2 Linux Instances
•	Flask mod_wsgi (Apache)
•	Apache Server Configuration Files
•	Deploy a Flask Application on an Ubuntu VPS
•	Set Up Apache Virtual Hosts on Ubuntu
•	mod_wsgi documentation
•	Automatic Security Updates 
•	Ask Ubuntu
•	Stack Overflow


