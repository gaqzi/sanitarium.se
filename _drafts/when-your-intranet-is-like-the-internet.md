---
author: björn
comments: true
date: 2015-10-20
layout: post
slug: when-your-intranet-is-like-the-internet
title: When your intranet is like the internet
categories:
- blog
tags:
- programming
- ruby
- devops
---

# When your intranet is like the internet

Do you remember the good old days? When people were honest and we all could
trust one another? The internet used to be like that once. Then
[September never ended] and things changed.

The good thing is that when you're on your own intranet then it's like in the
good old days. Your own little gated community. Safe and sound. Well, yes, up to
a certain size. Then your intranet starts looking a whole lot like the public
internet. Multiple data centers, several branch offices, some public access
terminals and some WiFi to keep it in sync. All of a sudden there's no practical
difference from the public internet.

Rails by default lives in the glory of the good old days, everything on my
network is safe and I can trust them. Which is a sensible configuration for most
apps. If you can't trust the traffic in your own datacenter then, well, you're
probably reading blog posts like this.

One of these settings for Rails is the algorithm it uses to figure out what the
remote IP address is for the current request. By default this is done by
removing all [private IP addresses] from the [X-Forwarded-For] header, inverting
the order of the remaining IPs and then picking the first unknown IP. The logic
for all of this is in the [ActionDispatch::RemoteIp] middleware which is used
to. To learn more about how the middleware works and why it does it the way it
does, then read the excellent blog post
[Rails IP Spoofing Vulnerabilities and Protection].

## Our setup

In our case what ended up happening was that all requsts appeared to be coming
from our load balancer, which can hardly be called an end user. Our app setup is
very straightforward. Some app servers, a load balancer, and in front of all of
this there’s a reverse proxy that handles SSL termination and routing for the
different apps this datacenter provides.

<img src="http://i.imgur.com/dSymXXD.png" 
     title="a simplified diagram of our datacenter"
     style="max-width: 500px;"
     class="center-block">

This datacenter lives in the `10.0.1.0/24` subnet. All our users come from
various other parts of the private IP space . All in all a request can hop
through up to five proxies and load balancers before reaching our app, each
adding the `X-Forwarded-For` header as traffic flows through it.

And because all the IP addresses in the `X-Forwarded-For` header are private
Rails will strip them. And when there's no addresses in `X-Forwarded-For` Rails
returns the `REMOTE_ADDR` instead. Which'll be the last visited node before the
webserver, in our case the load balancer.

## The solution

To work around this:

1. We got a list of all proxy ips/server subnets which we know no end-users will
   be accessing from
2. Installed the [Remote IP Proxy Scrubber] gem , which was built to handle this
   situation on the public internet. Like when you use CloudFlare in front of
   your app.
3. Configured the `ActionDispatch::RemoteIp` middleware to only ignore
   localhost by default, because if you can’t trust yourself…

```ruby
# This is config/environments/production.rb

# First off swap out the original ActionDispatch::RemoteIp middleware with
# our own configured version
config.middleware.swap(
  ActionDispatch::RemoteIp,
  ActionDispatch::RemoteIp,
  false,  # Don't perform any IP spoofing checking
  %r{
    ^127\.0\.0\.1$ |  # localhost IPv4
    ^::1$             # localhost IPv6
  }x
)

TRUST_PROXIES_AND_SUBNETS = %w{
  # All servers in the datacenter is trusted to report the correct IP
  10.0.1.0/24
  # Proxy server in office A
  10.1.1.10
  # Proxy server in office B
  10.1.2.10
}

# Filter out any known proxies and trusted subnets
config.middleware.insert_before(
  Rails::Rack::Logger,
  RemoteIpProxyScrubber.filter_middleware,
  TRUSTED_PROXIES_AND_SUBNETS
)

# Now to log the correct IP address, note this is added after ActionDispatch::RemoteIp, 
# so the IP has had a chance to be set
config.middleware.insert_after(
  ActionDispatch::RemoteIp, 
  RemoteIpProxyScrubber.patched_logger
)
config.middleware.delete(Rails::Rack::Logger)
```

Now Rails will believe that our intranet is just another part of the internet,
with a few select trusted sources. And we're able to see our user's IP
addresses. We can really see that there has been no traffic from building C all
day, and it's not just that caller having issues connecting to our app.


[private IP addresses]: https://en.wikipedia.org/wiki/Private_network
[X-Forwarded-For]: https://en.wikipedia.org/wiki/X-Forwarded-For
[Rails IP Spoofing Vulnerabilities and Protection]: http://blog.gingerlime.com/2012/rails-ip-spoofing-vulnerabilities-and-protection/
[ActionDispatch::RemoteIp]: https://github.com/rails/rails/blob/4-2-stable/actionpack/lib/action_dispatch/middleware/remote_ip.rb#L26
[Remote IP Proxy Scrubber]: https://github.com/metavida/remote_ip_proxy_scrubber
[September never ended]: https://en.wikipedia.org/wiki/Eternal_September
