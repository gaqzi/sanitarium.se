---

author: björn
comments: false
date: 2015-10-27 08:00:00 +08:00
layout: post
slug: testing-against-many-versions-of-python-on-snap-ci
title: Using multiple versions of Python on Snap CI
subtitle: Why just play with one snake?
categories:
- blog
tags:
- programming
- python
- gocd-cli
- snap-ci

---

I'm running an open source project called [gocd-cli] which is, well, a command
line interface for [Go continuous delivery]. The intention is to make it
easier to handle common tasks around Go. But this post isn't really about that.

This project is supposed to be as portable as I can make it, becuse the original
need I felt for it was born on RHEL6. Which is *blessed* with Python 2.6 by
default. And we should definitely be looking to the future, meaning supporting
Python 3, and I luckily got a [pull request] for just that. Since I couldn't
find any free hosted Go around I went for the next best thing, [Snap CI],
which is also built by [ThoughtWorks].

Easy to get going and works well, it's not Go, but it's definitely the easy
starter drug for people that thinks [Jenkins] or [Travis] is good enough.

## The solution

Snap supports all the versions of Python that I want by default, but they
weren't all being made available at the same time. Python 2.6 and 2.7
were always there, but only one version of Python 3 at a time.

Luckily logging in to the [snap-shell] I found that all Python versions were
available in `/opt/local/python/<version>`.

A quick change to the Snap config, to add these to my `$PATH`, and [tox] ran
through without any problems.

{{< img src="/img/2015/10/snap-console.png" alt="New Snap CI config" >}}

What you'll need to add to your command box. **Note** it didn't work for me when
I added it to the environment variable field, I'm guessing it's because the `$PATH`
variable doesn't get interpolated correctly.

``` bash
export PATH="$PATH:/opt/local/python/3.3.5/bin:/opt/local/python/3.4.0/bin:/opt/local/python/3.5.0/bin"
```

And look, my tests are passing!

[{{< img src="/img/2015/10/snap-success.png" alt="Passing tests" >}}](https://snap-ci.com/gaqzi/py-gocd/branch/master)

[gocd-cli]: https://github.com/gaqzi/gocd-cli
[pull request]: https://github.com/gaqzi/py-gocd/pull/6
[Go continuous delivery]: http://www.go.cd/
[Snap CI]: https://snap-ci.com/
[ThoughtWorks]: https://en.wikipedia.org/wiki/ThoughtWorks
[Jenkins]: https://en.wikipedia.org/wiki/Jenkins_(software)
[Travis]: https://en.wikipedia.org/wiki/Travis_CI
[tox]: https://tox.readthedocs.org/en/latest/
[snap-shell]: https://blog.snap-ci.com/blog/2014/08/11/introducing-snap-shell/
