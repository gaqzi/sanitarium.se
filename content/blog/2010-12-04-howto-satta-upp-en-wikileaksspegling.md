---
aliases: ["/blog/2010/12/howto-satta-upp-en-wikileaksspegling", "/blog/blog/2010/12/howto-satta-upp-en-wikileaksspegling/", "/blog/blog/2010/12/04/howto-satta-upp-en-wikileaksspegling", "/blog/blog/2010/12/howto-satta-upp-en-wikileaksspegling"]
authors: ['björn']
comments: true
date: 2010-12-04 21:27:26+00:00
lastmod: 2010-12-04 21:27:26+00:00
slug: howto-satta-upp-en-wikileaksspegling
title: "How to: Sätta upp en Wikileaksspegling"
language: se
wordpress_id: 327
categories:
- blog
tags:
- how-to
- linux
---

[A translation of this post is available in English.]({{< relref "2010-12-05-howto-setting-up-a-wikileaks-mirror.md" >}})

En [kommentar] i Rick Falkvinges inlägg [Fullt krig om informationen][infokrig]
så efterfrågades en snabbguide för att dra igång en Wikileaksspegling i ett
vanligt Linuxssystem.

Jag utgår från Ubuntu eftersom det är vanligt och vad jag själv använder.

**Uppdatering 2010-12-05:** Jag har gjort ett script som utför alla stegen nedan, använd gärna det!   
Filen: [http://sanitarium.se/files/wikileaks-mirror.sh](http://sanitarium.se/files/wikileaks-mirror.sh)  
Användning: `wget http://sanitarium.se/files/wikileaks-mirror.sh && chmod +x
wikileaks-mirror.sh && ./wikileaks-mirror.sh`

# Installera Apache
`#` är prompten som root:

```bash
dinanvändare$ sudo -s  
```

Installera apache om det inte är installerat

```bash
# apt-get install apache2  
```

Lägg till en användare för Wikileak och anteckna var wikileaks hemmap skapas!

```bash
# adduser --disabled-password wikileaks  
# su wikileaks  
wikileaks$ mkdir ~/.ssh ~/www  
wikileaks$ chmod 0700 ~/.ssh  
wikileaks$ wget http://213.251.145.96/IMG/id_rsa.pub -O ~/.ssh/authorized_keys  
wikileaks$ exit  
```

Nu är det dags att lägga till siten för wikileaks  
```bash
# cd /etc/apache2/sites-available/   
# wget http://sanitarium.se/files/wikileaks   
```

Öppna filen `wikileaks` med en editor och ändra sökvägen till användaren wikileaks hemmapp om det är något annat än `/home/wikileaks`.  
Den här filen förutsätter att du vill hosta wikileaks.org, om du vill hosta wikileaks.dindomän.se eller något sådant så får du ändra ServerName och eventuellt ServerAlias.  
När det är klart är det bara att aktivera siten för apache:  

```bash
# a2ensite wikileaks  
```

Och till sist ladda om apache så det är redo att ta emot information:  

```bash
# /etc/init.d/apache2 reload  
```

Innehållet i filen `wikileaks` som du tankar från den här servern är:

```text
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
```

# Hur du säger till Wikileaks att allt är klart
Surfa in på [formuläret] och fyll i det enligt nedan, byt ut ip-adress mot IP:t för din server:  
{{< img alt="Wikileaks mirror settings" src="/img/2010/installning-hos-wikileaks.png" >}}

Om det är några oklarheter eller funderingar så fråga på i kommentarsfältet
nedan så ska jag försöka hjälpa till att reda ut!

**Uppdatering:** [Henrik Rouhivuori](http://twitter.com/rouhivuori)
  upplyste om att `aptitude` inte finns i Ubuntu 10.10 så jag ändrade till `apt-get`
  istället. Övertydligt att jag fortfarande hänger på 10.04. :)

**Uppdatering 2:**
  Henrik Holst
  berättade att du kan välja att inaktivera lösenordsinloggning när du skapar
  nya användare, så nu görs det istället för att rekommendera ett slumpmässigt
  långt lösenord!

**Uppdatering 3:**
  David Vrensk
  påminner om att `sshd` är lite petig på att det bara är användaren som ska ha
  rättigheter till `.ssh`-mappen.

**Uppdatering 4:** Av bara farten så hade jag missat att lägga till att man
  måste skapa mappen `www` som wikileaks-filen pekar på, samt `common` efter
  loggraden. Tack till [Gustav Wetter] som jobbet igenom hela guiden!

[kommentar]:http://rickfalkvinge.se/2010/12/04/fullt-krig-om-informationen/#comment-57303
[infokrig]:http://rickfalkvinge.se/2010/12/04/fullt-krig-om-informationen/
[formuläret]:http://213.251.145.96/Mass-mirroring-Wikileaks.html
[Gustav Wetter]: http://harfagre.wordpress.com/
