---
aliases: ["/blog/2010/04/how-to-reactivate-calendar-notifications-on-your-htc-hero-if-they-stop-working", "/blog/2010/04/17/how-to-reactivate-calendar-notifications-on-your-htc-hero-if-they-stop-working"]

archived: true
authors: ['björn']
comments: true
date: 2010-04-17 12:59:03+00:00
slug: how-to-reactivate-calendar-notifications-on-your-htc-hero-if-they-stop-working
title: How to reactivate calendar notifications on your HTC Hero if they stop working
wordpress_id: 119
categories:
- English posts
tags:
- android
- calendar
- howto
- htc hero
- notifications
---



A couple of months back, out of the blue, my [HTC Hero] stopped notifying me on my upcoming calendar events. It didn't even show upcoming events on the home screen widget, but it kept syncing new events without a problem. 

I tried adding and re-adding the calendars I sync on the phone, turning on/off the notifications but nothing worked. I found a link to a guy who had the same problem, which ended up being caused by him force quitting the alarm service. But I had not done that, and either way it should've started working after a reboot if that were the case. Another guy managed to get his notifications working after doing a factory defaults reset.

Resetting to factory defaults isn't my first choice of action, so I searched for, [and found][link-to-source], a way to reset the calendar instead. And after doing that a test notification I set to go off a couple of minutes earlier got synced back to the phone and went off!

On your phone:

> Settings -> Applications -> Manage applications  
> Open up `Calendar storage` and press `Clear data`.  
> I also cleared the `Calendar` app, not sure if it was needed though. 

Posting in hope that if anyone else have this problem they won't have to rummage through the internet as I did.

[link-to-source]:http://androidforums.com/htc-hero/9828-delete-local-calendar-htc-hero.html#post55710
[HTC Hero]:http://en.wikipedia.org/wiki/HTC_Hero
