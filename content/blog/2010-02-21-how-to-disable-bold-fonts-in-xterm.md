---
aliases: ["/blog/2010/02/how-to-disable-bold-fonts-in-xterm", "/blog/blog/2010/02/how-to-disable-bold-fonts-in-xterm/", "/blog/blog/2010/02/21/how-to-disable-bold-fonts-in-xterm"]
authors: ['björn']
comments: true
date: 2010-02-21 22:36:19+00:00
location: Sweden
slug: how-to-disable-bold-fonts-in-xterm
title: How to disable bold fonts in xterm
subtitle: Why sometimes repeating yourself really does get the message through
wordpress_id: 67
categories:
- blog
tags:
- how-to
- linux
---

I've so far in all my travels never found a terminal I like better than [xterm], maybe [urxvt], but I've had a problem disabling bold fonts for a very long time. **Update:** Seems this is a [known bug for xterm][xterm-bug].

There are a lot of X resource configuration options that makes you think you can disable bold fonts, but alas, I've had no luck with any of them. But if you set **the same font** for both normal and bold fonts it'll work! This little gem of knowledge I found as an off-hand remark on a [configuration page][xterm-conf] by [Emil Mikulic][emil], thank you!

I like the normal `fixed` font, I've tried many terminal fonts but I've always gotten back to it. So I simply tucked:

    
    
    xterm*font: fixed
    xterm*boldFont: fixed
    



Into my `~/.Xresources` and afterwards ran `xrdb -load ~/.Xresources` and started up a new xterm loaded with awesomeness!  



{{< figure alt="xterm with bold font and xterm without bold font" src="/img/2010/xterms.png" >}}


The before and after shot.


[xterm-conf]:http://dmr.ath.cx/notes/xterm.html
[urxvt]:http://en.wikipedia.org/wiki/Rxvt-unicode
[xterm]:http://en.wikipedia.org/wiki/Xterm
[emil]:http://dmr.ath.cx/
[xterm-bug]:http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=347790
