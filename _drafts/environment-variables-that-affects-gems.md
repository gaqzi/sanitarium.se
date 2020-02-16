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

# Some system variables

`LANG` and the `LC_*` variables can really affect various parts of your system.
For a while [grep used to have a bug] when `LANG` was set to something with
`UTF-8`.

At work we found an interesting issue where the interpreter, Python in that
case, thought it was running with the POSIX locale. Which is basically ASCII,
and which doesn't support UTF-8 characters. But how did that end up happening,
and why?

# How are environment variables set?
Normally when you're using your computer the environment variables are set when you start your shell. The shell that you start off with is called a "login shell" and has some special characteristics.

# When are they set?

# Why are they sometimes unset!?


[grep]: http://dtrace.org/blogs/brendan/2011/12/08/2000x-performance-win/
[bundler env]: http://bundler.io/v1.10/bundle_config.html

How are environment variables set?

When using your terminal your shell is by default started as a "login shell". The login shell prepares you to work by:

Loading your dotfiles (.bashrc, .zshrc)
Running system level startup scripts (/etc/profile.d/*.sh)
Which is why you `eval "$(rbenv init -)"` in your .zshrc gives you access to rbenv on the cli. And in a shell script you've to call it yourself.

How does rbenv, pyenv, virtualenvs and the like work?

To be able to talk about this I've to introduce `$PATH`. `$PATH` is a variable that holds all the "search paths" for where you can find your executables. Type `vim` in your shell and press enter. What then happens is:

The shell looks at all directories in `$PATH`, separated by colons (:)
Concatenates the path and the executable, lets call it `$full_path`
If `$full_path` exists and is executable it's executed
Or in code:

```

ENV['PATH']  # => '/Users/ba/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin'
executable = 'vim'

full_path = ENV['PATH'].split(':').find do |path|
  path = File.join(path, executable)

  File.exists?(path) && File.executable?(path)
end

exit 1 unless full_path
exec File.join(full_path, executable)

```

And to get your rbenv selected version of Ruby first… ensure it's early in `$PATH`.

It's elegant in it's simplicity. Put your interpreter first in your `$PATH`, and you're set. Unix fundamentals.

# When are they set?

# Why are they sometimes unset!?
