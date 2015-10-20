---
author: björn
comments: true
date: 2015-10-20
layout: post
slug: environment-variables-that-affects-gems
title: Environment variables that affects gems
categories:
- blog
tags:
- programming
- ruby
- devops
---
## The introduction


I've been working on a project which is going to live for a long time. No one is
surprised if it's going to be around for more than 10 years. I say that because
the reason we're building this system is to replace the previous system, which
started development in the late 90s.

Given that the project has a time scale and that we want to make sure we don't
get ourselves into trouble down the line, we've made sure as we go along that we
can deal with some things we know will happen. Amongst them upgrading between
Ruby versions.

We started the project running Ruby 2.0 and recently switched to 2.1, policy
dictates that we stay on old-stable. Don't want to get bitten by any unknowns
first. The switch to 2.1 was surprisingly straight forward as far the app goes.
We just updated our `.ruby-version` file, commited, waited for new RPMs to be
built and Bob's your uncle.

Although while that's a nice story, and what it looked like by the time we went
into production, it took a while to get there.

Funnily enough that was true for moving between 2.0 and 2.1.6, but then moving
to 2.1.7 when it came out was a bit more of a problem. The issues were all
around helper scripts that aren't packaged as full fledged ruby apps, but rather
as just scripts. A user install of the gems and then the scripts gets run.

## Environment variables

### Where does gems get installed to?

If you're running Ruby the gems are by default installed to the global gem path.
If you're root. *Or if you have sudo access.* This last bit came as a surprise,
because my gems started getting messed up with each other when a new point
release came out.

The gem installation path is defined by the `GEM_HOME` environment variable, and
that's the base path to where all gems will be installed. If you have it set any
gems installed by `gem` or `bundler` will go there, unless overridden on the
command line.

The interesting bit here is that whenever there's a new release it's always good
to reinstall any compiled gems, they may not run with the new version. But the
gems are always installed to a folder for the `major.minor` and not
`major.minor.point` release. Which means that the next time around when you're
doing `bundle install` for your app it'll say that your compiled gem is
installed and everything is fine, but it's not at all fine. It's just crashing.

To work around this I've for now added a default `GEM_HOME` definition to our
rbenv init script to use the exact release of the global ruby version in the
path of the gem home. To be exact, `~/.gem/rubies/<2.1.7>` where `<2.1.7>`
represents the current ruby version. Now this only works when your app is using
the same version of Ruby as the global, as the value doesn't get re-evaluated
when you switch to another Ruby version, so at times you may need to set your
own path. In CI where we test multiple versions I've configured bundler to
install it by:

```bash
$ bundler install --path=$HOME/.gem/rubies/$(ruby --version | cut -f 2 -d ' ' | cut -f 1 -d p)
```

One tip for installing the gems though is to bundle them with `bundle
--production` and ship them "already installed" with your RPMs. It saves time
and makes it really fast to move between versions of your app. Even ones which
includes changes in your Ruby version.

### What gems to install?

Do you know that there's a bunch of environment variables that drastically
changes the way bundler and gems work? For instance, if you're starting a Ruby
script through `bundle exec` and then try to spawn a sub process. Then that sub
process will by default use the same `Gemfile` as the first process. Even if the
subprocess is in another folder and doing `bundle install`.

The magic behind that behavior is the `BUNDLE_GEMFILE` environment variable. The
idea is good and it's part of what makes bundler work so seamlessly. But if you
don't know about it then it can get annoying.

Just unset it in your subprocess and you can be merrily on your way.

There a full listing of the
[environment variables bundler is configured with][bundler env] on the bundler
website. Scroll down to "List of available keys".

[bundler env]: http://bundler.io/v1.10/bundle_config.html
