---
authors: ['björn']
date: '2025-08-13T08:28:11+08:00'
lastmod: '2025-08-13T08:28:11+08:00'
title: 'Use Commas as Prefix for Your Scripts'
tags:
  - shell-scripting
  - productivity
daily: ['2025-08-13']
---
[Commands with commas](https://rhodesmill.org/brandon/2009/commands-with-comma/): I came across this a couple of years ago, and I've been using it for [my new scripts since.](https://github.com/gaqzi/conf/tree/master/bin)

> Debian today supports a huge number of commands; my modest Ubuntu laptop shows several thousand available:
>
>>  $ apt-file search -x '^/usr/bin/[^/]*$' | wc -l  
>> 21733
> 
> The solution was obviously to adjust my command names in such a way that they were still easy to type, but would never be chosen as system command names.  
> […]
>
> **There was but one character left: the simple, modest comma.**
> 
> A quick experiment revealed in a flash that the comma was exactly the character that I had been looking for! Every tool and shell that lay in arm's reach treated the comma as a perfectly normal and unobjectionable character in a filename.[…]
> 
> And, best of all, **thanks to the magic of tab-completion, it became very easy to browse my entire collection of commands**. […]  
> I simply type a comma followed by tab and my list of commands appears


