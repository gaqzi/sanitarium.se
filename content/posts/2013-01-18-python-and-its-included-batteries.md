---
author: björn
comments: true
date: 2013-01-18 16:22:32+00:00
slug: python-and-its-included-batteries
title: Python and its included batteries
wordpress_id: 460
categories:
- blog
tags:
- python
- programming
---

I've for almost a year now been using [Python] as my day to day language as it's
what is used at my job. I'm starting to come around to really liking most parts
of Python now, although there is definitely parts that are way more clunky than
I would expect from a language so popular. And especially given how much talk
there's about the _[included batteries]_ and to a small extent how there seems
to bit of dickishness involved with hard core Python people. For an example of
the latter just:

{% highlight bash %}
$ python  
>>> exit  
Use exit() or Ctrl-D (i.e. EOF) to exit
{% endhighlight %}

Clearly the interpreter known what I want to achieve, and at the same time it's
programmed to give of an error message telling me I was doing it wrong. And for
it to work I need to say, "pretty please". What annoys me with this is just the
simple fact that someone figured out people were having a problem with this, so
they added in a message instead of just doing what is expected. You just don't
behave in that way in everyday life, you'd get slapped.

## Standard library

Time handling in Python is atrocious, do get it working halfway decently you
need to install at least two external libraries. [pytz] and [python-dateutil],
and while I can understand why pytz might be a good candidate for being external
(for allowing a higher pace of updates since timezone/[DST] changes happens
every so often in different parts of the world).

Today I just wanted to do a diff between two dates and see the years between
them, so I figured I would use [timedelta] since it sounds like something that
should be part of that. Oh, really, it's not? I can diff weeks but not months or
years? So I ended up using dateutil's [relativedelta] instead.

So far the worst way I've been bitten was with the built-in e-mail library, this
ended up with me sending a copy of the e-mail addresses of 150 customers by
mistake.

{% highlight python %}
import smtplib
from email.mime.text import MIMEText
  
msg = MIMEText('Ho ho ho, merry christmas')
msg['Subject'] = "You're wished something special!"
msg['From'] = 'noreply@otherdomain.tld'
msg['To'] = 'user-1@domain.tld'
msg['To'] = 'user-2@domain.tld'
  
print msg.as_string()
{% endhighlight %}

Output:

{% highlight text %}
Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: You're wished something special!
From: noreply@otherdomain.tld
To: user-1@domain.tld
To: user-2@domain.tld
   
Ho ho ho, merry christmas
{% endhighlight %}

Because appending when doing an assignment is just what you'd expect. This from
the same people that needs to tell me I can't type `exit` but I need to type
`exit()`.


Another thing I wanted to use was a windowing function when iterating over a
list, instead of having it implemented in [itertools] the documentation for
itertools explains how I can
[implement my own](http://docs.python.org/release/2.3.5/lib/itertools-example.html).
Why!? If you're taking the time to show of an implementation why should I have
to copy that piece of code into my own codebase? What about [The Zen of Python]:

> There should be one-- and preferably only one --obvious way to do it.

### PEP8

I really like [PEP8], I don't agree with all parts of it but I can change. But
I'm really looking forward to when the standard library finally is PEP8
compliant.

## Documentation

Which brings me to documentation. For the longest time I couldn't understand why
I had such problems understanding the Python documentation, whether it was the
standard library or any third party library. When I was coding [Ruby] I never
felt this stupid when reading documentation. (But I've been told I'm excused
from feeling stupid when reading the [SQLAlchemy documentation], apparently it's
not just me there.)

But I think I've figured it why I find the documentation so hard to understand
now. When I'm reading documentation for Ruby I generally have the source code
just one mouse click away. So when I wasn't understanding what the documentation
was saying I just flipped on the source code and I could figure it out.

{{< img alt="Ruby documentation source example" src="/img/2013/Screenshot_2013-01-19_00_30.png" >}}

With most Python libraries I've had to do something similar to this:

* Dig through to wherever the source is saved
* Find the correct version for the documentation I'm reading(missed version of source I'm reading more than once)
* Find exactly where this thing I want to read about is is defined. 
* Start reading the source
* ???
* Enlightenment.

It's a general "truth" that documentation in general sucks, so it's just better
read the source. But somewhere along the way I stopped doing that, probably
around the same time I started using Rails and was amazed at how good the
documentation was. And without thinking about it I was also already reading the
source code, kind of, by having it readily available with the documentation.

My recommendation is for all of you out there using [Sphinx] for your
documentation needs, please enable
[sphinx.ext.viewcode](http://sphinx-doc.org/latest/ext/viewcode.html) to output
the source with your documentation.

The other thing I would like to say is the obvious thing, reading the source is
great. I really started to enjoy using Django when I decided to just use the
documentation to find whatever something was called and then use the source code
to figure out how things work. Source code is almost like a painting, a line of
code can say more than a thousand words. ;)

## Wrapping up

I'm not the first one to feel dismayed about Python, [Zed Shaw] has a great post
called
[Curing Python's Neglect](http://zedshaw.com/essays/curing_pythons_neglect.html)
that is well worth a read. (He mentions Lamson 0.9 in the post and that was
released in 2009. As far as I can tell most of the things in his post is still a
problem.)

As I understand a lot of making Python more streamlined is being put into Python
3, that just hasn't been adopted by the majority of developers yet.

We Ruby people had the same thing with 1.9, and I noticed people really starting
to switch about the same time as [RVM] started to be used. All of a sudden there
was a really easy way to test things with any possible combination of Ruby you
wanted.

All around I'm really enjoying working with Python, again (Python was the
language I used to replace PHP/Perl way back when, then Python was replaced by
Ruby). I used to really dislike having to import every single line of code I
use, but since I'm a sucker for having things overly clear I've gotten round to
it now. For some reason I never had an issue with the white spaces, I want the
code I read to be consistent. And that's one way of trying to ensure that.

Now that I've done the virtual variant of screaming out into the night I'll go
and try to be productive instead.

{{< img alt="Classy Python" src="/img/2013/classy-python.png" >}}


[Ruby]:http://en.wikipedia.org/wiki/Ruby_(programming_language)
[Python]:http://en.wikipedia.org/wiki/Python_(programming_language)
[pytz]:http://pytz.sourceforge.net/
[python-dateutil]:http://labix.org/python-dateutil
[timedelta]:http://docs.python.org/2/library/datetime.html
[relativedelta]:http://labix.org/python-dateutil#head-ba5ffd4df8111d1b83fc194b97ebecf837add454
[DST]:http://en.wikipedia.org/wiki/DST
[itertools]:http://docs.python.org/2.7/library/itertools.html
[The Zen of Python]:http://www.python.org/dev/peps/pep-0020/
[Sphinx]:http://sphinx-doc.org/
[RVM]:https://rvm.io/
[included batteries]:http://www.python.org/about/
[PEP8]:http://www.python.org/dev/peps/pep-0008/
[SQLAlchemy documentation]:http://docs.sqlalchemy.org/
[Zed Shaw]: http://zedshaw.com/