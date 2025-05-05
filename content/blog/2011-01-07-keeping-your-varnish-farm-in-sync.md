---
author: björn
comments: true
date: 2011-01-07 01:21:46+00:00
slug: keeping-your-varnish-farm-in-sync
title: Keeping your Varnish farms configuration in sync
wordpress_id: 378
categories:
- blog
tags:
- varnish
- linux
- devops
---

I spend some of my free time helping out with server administration and
programming for the [Swedish Pirate Party][pp-wiki], [Piratpartiet] (*look ma*,
X-Varnish), and we use [Varnish] for our caches. At the moment it's just used on
some of our projects, but we're going to migrate most of our projects to be
behind our Varnish caches.

The thing is though that we got two hosts running the exact same configuration,
and we'd like to keep those hosts in sync. A quick search on Google gave me
nothing for syncing varnish configuration over several hosts, or a farm as it
were. So I took matters into my own hands and wrote [varnishsync], a little bash
script that uses rsync and ssh to sync the configuration folder and then to load
and use the new configuration.

Please have a look at the [Github project][varnishsync] for the latest version
and usage, and if you've any questions or suggestions drop a line here or on
Github.

[pp-wiki]:https://secure.wikimedia.org/wikipedia/en/wiki/Piratpartiet
[Piratpartiet]:http://www.piratpartiet.se/
[Varnish]:http://www.varnish-cache.org/
[varnishsync]:https://github.com/gaqzi/varnishsync