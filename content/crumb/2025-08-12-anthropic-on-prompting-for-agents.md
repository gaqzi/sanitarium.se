---
authors: ['björn']
date: '2025-08-12T23:53:04+08:00'
lastmod: '2025-08-12T23:53:04+08:00'
title: Anthropic on prompting for agents
subtitle: …and musing on genies possibly teaching empathy
tags:
  - genie
  - mentoring
  - context-engineering
  - kent-beck
series: ['learning-with-genies']
daily: ['2025-08-12']
---
Anthropic has released some recordings from their Code w/ Claude event in May and the [Prompting for Agents](https://www.youtube.com/watch?v=XSZP9GhhuAc) presentation's "key principles" are basically to _empathise_ with your agent, imagine it's a brilliant new grad, book smart but missing all things practical at their first job: You need clear concepts, unambiguous instructions, and well-named and designed tools.

{{< youtube XSZP9GhhuAc >}}

I'm more than a little amused that we're basically coming to a point where, if things pan out with the genies, then the best wranglers will be the ones that can empathise the most with others. Then again, I always thought the brilliant asshole was the exception, they only survive if they're in charge or are legacy to the company. And sitting in on the review meetings at work… it's definitely the ones that help the team that we like the most, even if we sometimes need to push them to have their name on something so people don't overlook them.

If the genies take off, then I wonder what kind of knock-on effect it'll have on developers, and will it improve their interpersonal skills? What I have noticed is that my XP practices seem to be why I have better luck than some friends. Earlier this year, a chat kept generating wrong code, I decided to figure out why, and I realized I'd been inconsistent with my naming. The genie was mixing things up because I was mixing things up. Any human developer would've had the same problem working in this code. When I fixed the inconsistency, the genie immediately got it right. The same practices that make code maintainable make it genie-friendly.

And to me it's not first about genies, but the humans, and we already struggle with the human-to-human. Most of my thank-yous this year? Not for design help, but for helping people communicate their changes. Maybe because design feels closer to home, it's the skill they already have, just needs a nudge, and might've gotten there anyway. But communication? Underdeveloped. Might not have gotten there otherwise.

Just last week I heard someone saying they didn't need to provide context because "anyone reading this should know this already." But your ask is piling onto whatever they're already doing. The ideal? Create the context, set up the options, explain how to make the call based on their situation. And if they don't know? Give them the "just do this" default that works 90% of the time, no deep dive required. Same as with genies: do the setup work, make the ask trivial. Or as Kent Beck says about code: "Make the change easy, then make the easy change." Turns out that works when asking for help, too.
