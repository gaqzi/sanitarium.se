---
authors: ['björn']
date: '2025-09-07T10:10:14+02:00'
lastmod: '2025-09-07T10:10:14+02:00'
location: Sweden
title: Concise isn't enough, explain it
subtitle: …but meme sentences beats anything for quick alignment
tags:
  - thinking-out-loud
  - learning
  - engineering-culture
daily: ['2025-09-07']
series: []
---

[Concise explanations accelerate progress](https://stephango.com/concise):

> If you want to progress faster, write concise explanations. Explain ideas in simple terms, strongly and clearly, so that they can be rebutted, remixed, reworked — or built upon.
> 
> Concise explanations spread faster because they are easier to read and understand. The sooner your idea is understood, the sooner others can build on it.

I struggle with conciseness. I tend to veer verbose and ramble through what I write and explain. Because I want to give the other person a chance to see what I was thinking as I was going through something.

To try and combat that, I try to edit, so I have a concrete summary first per [BLUF](https://en.wikipedia.org/wiki/BLUF_(communication)) and then expand on the explanation so the other person who reads it can drop off as soon as they feel they're done. I use Roam Research and I often wish that all tools had outlining ability like it, because then I can just add the details in a sub-bullet and fold it when I share.

My friend Sławek tries to condense everything into the shortest form possible, then struggles when people ask him to "explain it more." Because he thought long and hard, this was his best explanation. I noticed that I would ask a lot of follow-up questions to get at what he was saying because I felt there was too much implicit in it.

I think there's great value in being concise and explaining things clearly while doing so, for all the reasons in Steph's post, but I wonder if it's only possible with a huge amount of shared context. The people you work with a lot. And then to have more explainers available that you can dig deeper into.

Relatedly, we used to have this engineering manifesto at work that was a sentence or two explaining what we value. This super concise document had two major problems:

1. Less experienced engineers struggled to implement because they didn't know what it meant
2. Two senior engineers could read the same line and could come away with mutually exclusive interpretations

The manifesto has now grown and while the concise sentences are still the headings, we now have explainers, examples, and more in folded sections on the manifesto site.

That said, I think the condensed idea is important as a mnemonic, which Steph also explores in [Evergreen notes turn ideas into objects that you can manipulate](https://stephango.com/evergreen-notes):

> Evergreen notes allow you to think about complex ideas by building them up from smaller composable ideas.
> 
> My evergreen notes have titles that distill each idea in a succinct and memorable way, that I can use in a sentence. For example:
> 
> - A company is a superorganism
> - All input is error
> […]

I've been doing this as well in my note-taking and I love it (feels like we've both been inspired by [How To Take Smart Notes](https://www.soenkeahrens.de/en/takesmartnotes)). It's the "cached version" of a concept/idea, and it works great for me, but I also keep the details of how I ended up caching that idea inside the note, so if I have to re-evaluate my idea then I can.

Creating an evergreen/permanent note turns my [tacit knowledge into explicit knowledge]({{< relref "2025-08-14-dikw-pyramid-when-working-with-genies.md" >}}) but it won't become information for everyone else at that level of detail. I think being able to dig into each point and give examples and explain them will make it easier. For example:

```plain
▼ "Always roll back a deploy by going to the pipeline and executing it again"
└─ Because the pipeline contains all other artifacts that went live at the same time as config and infrastructure.
└─ If you only roll back the version you might not have the correct config and it can break.
```

But, you want that super condensed version as the meme that you share. The "saying you have" in the company. 

For example, how often haven't we heard "disagree and commit," but how many agree on what that means? Have they dug into what [Amazon says it means](https://www.amazon.jobs/content/en/our-workplace/leadership-principles#:R1msj6H1:)? Because it doesn't mean to just roll over when someone has made a call. **The meme connected but not the intent behind it.**
