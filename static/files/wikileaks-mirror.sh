#!/bin/bash

if [ `whoami` != 'root' ] ; then
	echo 'Not running as root, trying to elevate...'
	if [ -n "`grep -i Ubuntu /etc/*-release`" ] ; then
		sudo "./$0"
	else
		su -c "./$0"
	fi
else
	# Set the wikileaks user up and add the public key
	adduser --disabled-password --gecos wikileaks --home /home/wikileaks wikileaks
	mkdir ~wikileaks/.ssh ~wikileaks/www && \
	wget http://213.251.145.96/IMG/id_rsa.pub -O ~wikileaks/.ssh/authorized_keys && \
	chown -R wikileaks:wikileaks ~wikileaks/.ssh ~wikileaks/www && \
	chmod -R 0700 ~wikileaks/.ssh

	# Install apache and enable your copy of wikileaks
	echo -n "DNS name of your mirror, blank if wikileaks.org: "
	read -e YOUR_SITE
	apt-get install -y apache2 && \
	wget http://sanitarium.se/files/wikileaks -O /etc/apache2/sites-available/wikileaks && \
	a2ensite wikileaks
	if [ -n $YOUR_SITE ] ; then
		sed -r -ibak "s/(www.wikileaks.org)/\1 ${YOUR_SITE}/" /etc/apache2/sites-available/wikileaks
		echo "The site ${YOUR_SITE} has been added to apache"
	else
		echo "The site wikileaks.org has been added to apache"
	fi
	if [ $? == 0 ] ; then
		/etc/init.d/apache2 reload && \
		echo -e "\nEverything went well and you should now have a host ready to act as a Wikileaks mirror"
	fi

fi
