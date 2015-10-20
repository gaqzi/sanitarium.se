---
author: björn
comments: true
date: 2010-12-05 21:11:18+00:00
layout: post
slug: howto-setting-up-a-wikileaks-mirror
title: 'How to: Setting up a Wikileaks mirror'
wordpress_id: 366
categories:
- blog
tags:
- howto
- linux
- piratpartiet
- wikileaks
---

Yesterday I wrote a quick step-by-step guide for installing apache and setting
your system up for [Wikileaks mass-mirror project][formuläret] in Swedish and
I've had requests for it to be translated into English.

This guide assumes you're running Ubuntu or a Debian based system.

I've made a script that does all the steps below, feel free to use it!  
The script: [http://sanitarium.se/files/wikileaks-mirror.sh](http://sanitarium.se/files/wikileaks-mirror.sh)   
Usage: `wget http://sanitarium.se/files/wikileaks-mirror.sh && chmod +x wikileaks-mirror.sh && ./wikileaks-mirror.sh`

# Installing Apache and adding the wikileaks user
`#` is the prompt as root:  
>> youruser$ sudo -s  

> Install apache if it's not installed  
>> `#` apt-get install apache2  

> Add a wikileaks user, write down where the home folder is created.  
>> `#` adduser `--`disabled-password wikileaks  
>> `#` su wikileaks  
>> wikileaks$ mkdir ~/.ssh ~/www  
>> wikileaks$ chmod 0700 ~/.ssh  
>> wikileaks$ wget http://213.251.145.96/IMG/id_rsa.pub -O ~/.ssh/authorized_keys  
>> wikileaks$ exit  

> Time to add the apache site for wikileaks  
>> `#` cd /etc/apache2/sites-available/   
>> `#` wget http://sanitarium.se/files/wikileaks   

> Open the file `wikileaks` with an editor and change the path to the wikileaks users home folder if it's not `/home/wikileaks`.  
> This file assumes you want to host wikileaks.org, if you want to host wikileaks.yourdomain.com you'll need to set `ServerName` accordingly and if necessary `ServerAlias`, ServerAlias is optional and you can remove that row if you don't use it.  
> When that is done you just need to activate the site in apache:  

>> `#` a2ensite wikileaks  

> And reload apache so it knows that the new site has been added:  

>> `#` /etc/init.d/apache2 reload  

The `wikileaks` file downloaded from this server looks like this:

    <VirtualHost *:80>
            DocumentRoot /home/wikileaks/www
            ServerName wikileaks.org
            ServerAlias www.wikileaks.org
            ErrorLog /dev/null
            CustomLog /dev/null common
    
            <Directory /home/wikileaks/www>
                    AllowOverride None
            </Directory>
    </VirtualHost>
    
# Now tell Wikileaks about your mirror
Go to the [form][formuläret] and fill it as the picture, set the IP-address of your server in the IP-field:  
[![](/img/2010/installning-hos-wikileaks.png)]({{ site.url }}/img/2010/installning-hos-wikileaks.png)

If you're having any troubles don't hesitate to ask in the comments!

[formuläret]:http://213.251.145.96/Mass-mirroring-Wikileaks.html
