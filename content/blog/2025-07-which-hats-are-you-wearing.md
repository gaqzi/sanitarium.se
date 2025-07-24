---
author: 'björn'
date: '2025-07-12T15:06:00+08:00'
lastmod: '2025-07-12T15:06:00+08:00'
title: Which hat are you wearing?
subtitle: ...you wouldn't wear a beanie to the beach
tags:
  - production
  - incidents
  - thinking
  - roles
  - leadership
---

I was in an incident review recently where one of the problems was a human going too fast. This process is very manual, repetitive, and boring, and it rarely fails, so we skip some steps. That mostly works (see [Why Do Things Go right?](https://safetydifferently.com/why-do-things-go-right/)), except when it doesn't. Ripe for occasional issues and likely in need of automation.

I believe we often skip steps because we don't know *why* we do them. It's not tedious for tediousness sake, it's [often there because it's important](https://fs.blog/chestertons-fence/). And until we have the automation, or maybe we've intentionally chosen not to automate it, we need to find some way of helping the human 'live the situation.'

Which reminded me of this Terry Pratchett quote: "Every trade, every craft had its hat. That's why kings had hats. Take the crown off a king and all you had was someone good at having a weak chin and waving to people. Hats had power. Hats were important."

And there's something to this, right? Like in my own role as a principal engineer, I am definitely *seen* as my role more often than I am the person beneath it. When people see me in a meeting, they see the title first. Hopefully I provide valuable insights and useful things. But even if I provide absolute garbage input, there's a significant chance people will listen, and maybe even not push back, because of the hat.

But, I have been wondering: what is your role and what is your ownership? What is it that you individually provide to whatever work you're doing? And is it always the same hat?

## The hat you don't know you're wearing

I think your hat changes depending on the role you're fulfilling at the moment. When you're working as a software engineer, you wear an engineering hat where you think about the feasibility of what you're building, like, can I maintain this thing long term, how far will it scale, and how testable is this design?

But if you're working as a product engineer, you're probably first thinking about how do I get this damn thing out the door, so you can see if it works or not. It's about trying things, slapping it together, flinging it against the wall with the smallest responsible amount of tests (so you know you don't break existing things when you iterate), and see what sticks.

I've noticed, though, that we often forget to switch hats when we need to.

Take deploying to production. When we're about to take something live, we should be wearing a different hat. We need to embody the spirit of production itself, become its guardian of stability (yeah, yeah, too many roleplaying games). Some orgs have a "release manager" as a dedicated role, but even if it's not a dedicated role, the need is always there. Taking things live is one of the most dangerous things we do: because most incidents happen when we change something. Whether it's config, a flag, or code.

The product engineer hat and the production guardian hat often feel very similar, and that's exactly the problem. Just because a hat _is similar_ doesn't mean _it's the same._ The product engineer wants the experiment live yesterday. The production guardian knows we can only ship today, and wants to make sure we still have a tomorrow. It's this impossible tension, one person wanting to have already finished something we haven't even started, the other pumping the brakes to make sure we don't break what's already working. And that often leads to "safety theater," where we do it a little bit slower, say 30m to get everywhere instead of one quick change, to catch disasters but not slow burn issues. Obviously this tension changes, to use [Kent Beck's 3X model](https://medium.com/@kentbeck_7670/the-product-development-triathlon-6464e2763c46), depending on whether you're in eXplore, eXpand, or eXtract mode. We're mostly in eXtract, so breaking things affects a lot of customers and the production guardian hat needs to be especially strong.

For example, in another incident, someone didn't manually check dashboards after deploying, which was part of the process, because they trusted the automated alerts. The alert came in after 10 minutes when it had enough data to be sure it wasn't temporary. But a human who was actually monitoring, really living that production guardian role, would've realized something was wrong within a minute or two. The manual step was there because the team knew their automated alerts weren't good enough to handle all issues around deployments.

Where I work today, we have some 250 backend components. We can test all we want, black box integration tests, contract tests, end-to-end tests, manual QA, all of it. We're still going to miss and get stuff wrong sometimes.

The point and our challenge in mindset is: when we're taking things into production, we're not wearing the hat of the product engineer anymore. We're taking on the role of production's guardian, and we're shepherding changes safely into production.

## It's like Vim modes, but for work

Say whatever you want about Vim, but one really nice thing is that it's modal. The idea that I'm now doing this thing (inserting or editing text), and now I'm doing this other thing (normal or moving and transforming), and you behave differently in those modes.

I see this in my own work all the time. I regularly review my own PRs because even though I went through everything when writing my commit message, I invariably look at it differently when I'm on GitHub in the interface I use for reviews. I switch much better into reviewer mode when I'm leaving comments there. It's common that I review and leave myself comments for what to fix, discover I need a comment, or elaborate a little bit further on something the reviewer might not be familiar with.

It's like TDD in a way. When you're red, you rush towards green by just getting it to work in the simplest way you humanly can. Then, when it's green, when you got it working, you refactor it. Different modes, different goals.

We need to be more intentional about which hat we're wearing at the moment.

## Becoming the character

I saw this story about Christian Bale recently (and look, I can't find the original source, so this might be one of those stories that's too good to fact-check, but it perfectly captures what I'm talking about). He's a famous [method actor](https://en.wikipedia.org/wiki/Method_acting), someone who becomes their characters completely. Apparently, when he wasn't getting much work, he dreaded having to read through his insurance contract and have that conversation because it was boring.

But then he decided: if I were a character who really cared about understanding insurance thoroughly, who would want to have an informed conversations about it... So he became that character and called up his insurance company. Apparently, they'd never talked to someone so well-researched on their contract.

And that's the thing, we kind of need to do this throughout our day. When you're taking something live, you're not the "ship fast" product engineer anymore. You have the right to say no, the right to say this has to be done slower because of these risks. Your responsibility is to make sure production is stable and things will continue to work.

## The $9,999 skill

There's this [great story about Charles Steinmetz](https://www.smithsonianmag.com/history/charles-proteus-steinmetz-the-wizard-of-schenectady-51912022/) and Henry Ford. Ford's engineers couldn't fix a generator problem, so they called in Steinmetz. He spent two days just listening to the generator and scribbling calculations. Then he climbed up, made a chalk mark, and told them to replace sixteen windings at that exact spot. It worked perfectly.

When Ford got the $10,000 invoice, he asked for an itemized bill. Steinmetz sent back:
- Making chalk mark: $1
- Knowing where to make mark: $9,999

And think about what Steinmetz did: he could have torn the whole generator apart, called in a team of engineers, or tried a dozen different approaches. Instead, he recognized this was a moment for careful analysis. He spent time listening, thinking, calculating. He put on his expert diagnostician hat, not his collaborative problem-solver hat or his hands-on mechanic hat.

And this is it exactly. Knowing where to make the mark, **knowing which hat to wear when, that's the $9,999 skill.**

But it's not just about perspective: each hat comes with different expectations, different powers, different rights, and different responsibilities. The production guardian has the authority to halt deployments. The incident responder can stop all feature work immediately. The planning hat carries the responsibility to think long-term even when it slows things down. When you put on a hat, you're not only changing how you think and approach the situation: you're claiming the legitimate authority that comes with that role.

I think that we often fail not because we lack skills, but because we're wearing the wrong hat for the moment. Or worse, we're trying to wear all the hats at the same time.

The product engineer hat wants speed. The production guardian hat wants stability. The incident responder hat wants recovery. The planner hat wants predictability. These aren't compatible mindsets, you can't optimize for all of them simultaneously. The goal is to negotiate productively across them, which is hard as one person, and, this is also why working through problems with others is so powerful.

```plaintext
THE INCOMPATIBLE MINDSETS
Product Engineer  
  → Wants speed (ship it yesterday)
Production Guardian
  → Wants stability (safety today, here tomorrow)
Incident Responder
  → Wants recovery (fix it now)
Planner           
  → Wants predictability (sustainable pace)
```

So here's what I've been trying to do, or rather, what I should start doing: be explicit about which hat I'm wearing. Right now I say things like "okay, from a stability POV" before raising concerns about deployment risks. But I should actually say, "let me put on my **production guardian hat** for a second." It helps others understand which perspective I'm bringing, and it helps me focus on what matters for that role.

## Tying it on

I think there's more to the hats we wear throughout the day because it's not just at work: supporting partner, fun uncle, mentor, learner. Each comes with different expectations, powers, and responsibilities.

But for now, I'll leave you with this: What hat are you wearing right now? What are the expectations that come with it? What responsibilities? And more importantly, is it the right hat for what you're trying to do?

Because understanding when to switch might be one of the most underrated skills we need. I'm currently convinced that being intentional about our roles, knowing which hat we're wearing and when to change it, that makes a difference. Not between being good or great, but between solving the right problems and creating new ones.

What would change my mind is if someone showed me that this context-switching has too much overhead. But, I think these aren't the context switches we usually complain about, the ones that kill our flow when we jump between meetings and deep work. These switches are within the same context we're already working in. We're just tilting our perspective, changing how we evaluate the situation. And in my experience, the cost of wearing the wrong hat is far higher than the cost of being intentional about switching.
