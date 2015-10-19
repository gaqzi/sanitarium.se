---
archived: true
author: björn
comments: true
date: 2010-09-28 17:07:24+00:00
layout: post
slug: how-to-disable-spotify-from-making-p2p-connections-in-windows-xp
title: 'How to: disable Spotify from making P2P connections in Windows XP'
wordpress_id: 238
categories:
- English posts
tags:
- firewall
- howto
- networking
- spotify
- windows
---

I've been having trouble at work with the available bandwidth running out when I and my co-workers are using [Spotify], a very nice piece of software, [but just like Skype][skype-bw] it tries to split its content through all available nodes and make sure they share it, which includes its users.

So what I did to force Spotify to only connect and fetch data from the Spotify servers was to use the built-in firewall in Windows XP and specify that `spotify.exe` is only allowed to connect to: [`78.31.8.0/22,193.182.8.0/21`][spotify-servers], mix up some traffic priority rules at the router for connections to those IP:s and Spotify can still be used, and not taking up all available bandwidth.

[![](http://sanitarium.se/blog/wp-content/uploads/2010/09/spotify-firewall-updated-255x300.png)](http://sanitarium.se/blog/wp-content/uploads/2010/09/spotify-firewall-updated.png)

**Updated 2011-08-23**: Added a new IP-range that Spotify uses, 193.182.8.0/21.

[skype-bw]:http://forum.skype.com/index.php?showtopic=16251
[Spotify]:http://spotify.com
[spotify-servers]:http://getsatisfaction.com/spotify/topics/how_can_i_block_spotify_on_our_company_firewall
