---
authors: ['björn']
date: '2025-08-24T13:25:00+08:00'
lastmod: '2025-08-24T13:25:00+08:00'
location: Singapore
title: Reasonable assumptions
subtitle: …and why they're (nearly) impossible
tags:
  - thinking-out-loud
  - engineering-culture
  - remote-work
daily: ['2025-08-24']
---

As I was writing up [angry at the genie]({{< relref "2025-08-24-angry-at-the-genie.md" >}}), about getting frustrated at a bot for not having my context, I realized I'd done the same thing to a human colleague just months earlier.

A new colleague has been speed-running _five years of my accumulated context_, and I was getting _really annoyed_ at all their questions. Why weren't they making any reasonable assumptions? They're a human after all, with decades of experience. In hindsight, I think that's exactly why they're not assuming and instead clarifying.

Because I've also been annoyed when new people come in "guns blazing" with their great ideas without learning about our context first. (I did this myself after leaving Pivotal Labs, came into my next job pushing XP and TDD. It went over about as well as you'd expect. Many of my pivoted friends seems to have had the same problem.)

So which is it? Make assumptions or don't? I want both and neither, apparently. Good going on consistency there.

I apologized for getting annoyed and letting it show. Told them I was catching myself getting annoyed and it's about me, not them, so please keep up the questions. Feel free to call me out if I'm starting to sound annoyed because I need to do better. I have nearly five years of context, failed and successful projects, and of course they can't capture that in a few months. And this person and I at least have the benefit of working in the same office (on days we go in) and timezone.

Now, making it worse is that as a company we're split across timezones: Central Europe and Singapore, so most of our communication happens in text. We only have 2-3 hours a day of natural overlap, which makes meetings _hard_. You often end up having first interactions with people purely in text. And it gets messy.

Someone trying to solve a problem will come in with their idea of the world and not have enough context, and that back and forth can easily feel like it's becoming heated for whoever is under time pressure, and the pressure builds because you'll often only get one round back and forth per day due to other meetings and obligations during the overlap.  
_Why don't they just understand what I need?_ "This person isn't trying to understand me" or "they're not trying to help me solve my problem." 

But they are. 

The other person is trying to extract enough context from what you want to do so they can actually help. The concrete thing you asked for (poke this hole in the firewall, add another 2 boolean fields into this payload) doesn't align with your actual goals, so they're trying to understand what you're *actually* trying to do, so the quick hack today isn't next quarter's blocker. Because the other teams have to take long-term maintenance into account for whatever decision gets made. You're focused on right-fucking-now, but they're going to own this forever.

[SwiftOnSecurity](https://infosec.exchange/@SwiftOnSecurity) has said that the best security team isn't the one that says no to keep you safe, it's the one that helps you get yes. Because if they can find a solution that solves your real problem, you're less likely to try and circumvent them. That's a whole lot more work, though. You have to empathize and understand your customer. You have to extract all that context. You have to balance their urgent need with your long-term ownership.  [Being curious enough to find correct rather than just being right.]({{< relref "2025-08-21-what-makes-a-good-software-engineer.md" >}}) 

And this isn't just about security teams, it's every interaction across teams and timezones. We're all, hopefully, trying to say yes while protecting what we own.

At the first job I had which was split across continents, we had a "remote working guide" and the first page said something like: "Always assume good intent from the other person, text makes it easy to put feelings in because you can't read the person and voice."

Despite internalizing that lesson, I get caught every so often getting emotional. Even with a damned bot. I put intent into text where there literally cannot be any. I assume malice, or at least incompetence, when really someone is just missing five years of accumulated context that feels like breathing to me. I mostly catch myself quickly and in text I can hide it, mask it with emojis, focus on the words. But in person? My tone undermines everything, no matter how rational my words are.

Something I heard, and keep thinking about, is that everyone's the hero of their own story. The job is trying to find where your story overlaps with theirs so you both can get the job done.

To try and connect stories we use [BLUF](https://en.wikipedia.org/wiki/BLUF_(communication)) and [the pyramid principle](https://medium.com/lessons-from-mckinsey/the-pyramid-principle-f0885dd3c5c7), formal ways of writing for clarity. We use them in remote/text-first work as pure survival: front-load everything and let people skip what they know. 

Add "if X then Y" answers to our questions when we assume a specific question to avoid the **24-hour wait**. Be direct without being an asshole. Don't waste time with false politeness, but don't be rude either. And still, that back-and-forth feels frustrating because what's obvious to you is an unfolding mystery to the other person.

So what are the reasonable assumptions that actually work? Some that I've found: 

- Assume good intent
- Assume they're trying to help
- Assume your context isn't obvious
- Assume you'll need to explain more than feels necessary
- Assume you need to signal that you're happy/helping by peppering liberally with emojis (you can't read the smile otherwise)
- And when you catch yourself getting frustrated, assume you need to apologize and reset

One more thing that helps: engage as we're merging contexts. "Are you saying X because Y? And therefore Z would be right out?" hits different than "what should I do?" or the umpteenth "why?" from a five-year old. The first shows you're engaging with the problem. The second sounds like you're expecting me to serve manna from the heavens. Even wrong thinking shows that we're working together.

So which is it? Make assumptions or don't? Turns out it's both and neither, just like I wanted 🙄. These "reasonable assumptions" assume the best of others while assuming nothing about what they know. Trying to resolve the contradiction by changing what we're assuming about, not their knowledge or context, but their intent and goodwill.

I keep learning this same lesson: with bots, with new colleagues, with anyone who hasn't been marinating in my context for years. You'd think I'd remember by now that my obvious is everyone else's mystery. But here I am, getting frustrated again when someone asks me to explain my obvious. Or getting equally frustrated when they assume _their obvious is mine._

