---
aliases: ["/blog/2009/08/webby-with-pingbacks-trackbacks", "/blog/2009/08/15/webby-with-pingbacks-trackbacks"]

archived: true
author: björn
comments: true
date: 2009-08-15 21:54:31+00:00
layout: post
slug: webby-with-pingbacks-trackbacks
title: Webby with pingbacks/trackbacks
wordpress_id: 11
categories:
- English posts
tags:
- ruby
- web standards
- webby
---



I decided I should have a blog to discuss or publish things I find interesting or otherwise on the Internet. Now the thing is that I also like having things fast, meaning that I think it’s nice if things are static. So enter [Webby](http://webby.rubyforge.org), easy to use, configurable and easily extendable, through [Ruby](http://en.wikipedia.org/wiki/Ruby_%28programming_language%29), and add the fact that webby generates static HTML, it can hardly get any better! :)

That is except for the community building part of having a blog, comments and the ability to tell other people automatically that I’ve written about a post of theirs or the reverse — someone else wanting to tell me that they’ve written about one of my posts.
So the first part of that puzzle I found was [Disqus](http://www.disqus.com) which is a javascript commenting system that can be used with any javascript enabled browser. So now I have comments, but [Disqus also do trackbacks](http://blog.disqus.net/2008/06/17/support-for-trackbacks-in-disqus/). But [Trackbacks](http://en.wikipedia.org/wiki/Trackback) are very spam prone and because of that the community came up with [Pingbacks](http://en.wikipedia.org/wiki/Pingback) instead. Pingback activated sites does some verification on the incoming links and if all of it checks out it then records it. So what I decided to do was to transform incoming pingbacks, through a proxy, to Disqus trackbacks. I think it’s a nice and simple solution. :)


## webby-pingback gem


So I created the [webby-pingback](http://github.com/ba/webby-pingback) gem which consists of two parts.



	
  1. A pingback client/sender. Using a new meta-data tag with your webby posts and a publish hook you can ping all links in your posts

	
  2. A pingback receiver/server. A CGI-script using Rubys built-in XML-RPC-library tries to act according to the [pingback protocol](http://www.hixie.ch/specs/pingback/pingback) and if all of it checks out OK it then sends a _trackback_ to the Disqus forum of the post.


So this is all pretty new and I’m hoping someone else will find this useful as well. I’ve added installation instructions at the [github repository](http://github.com/ba/webby-pingback) and I hope they are all pretty self explanatory.

If someone have any questions or comments please leave your mark below. :)

_I’ve since the original publication tried to clean up the language/wordings to try to make it more coherent :)_

_Update 2010-02-21: Since the posting of this post I've migrated over to Wordpress, while I love the idea with Webby I realized I also wanted to easily make a blogpost even if I were not at my own computer._
