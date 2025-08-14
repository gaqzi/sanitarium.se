---
authors: ['björn']
date: '2025-08-14T08:27:58+08:00'
lastmod: '2025-08-14T08:27:58+08:00'
draft: true
title: Angry at the Genie
subtitle: …on attributing intent when there is none
tags:
  - genie
daily: ['2025-08-14']
---
A colleague was saying that he'd like a genie coach to practice [first principles thinking](https://fs.blog/first-principles/), because they'd heard about the cooking coach I've been using, so I decided to give it a try and whipped up a prompt and gave it a spin.

I had a problem I had been working on which I wanted to see if there was some other way of thinking about it, and I also asked it to add in [behavioral economics](https://en.wikipedia.org/wiki/Behavioral_economics) as an angle because I've been interested in trying to pull in a more human angle to my thinking (which it seems to fit, I'm still learning).

I set the prompt up to force me to reflect on how I'm working and that I want to try and explain myself, because I figured that'd be the way for me to learn. So we started, the thing I explained was total garbage, I was fundamentally doing too much, and needed to do less work. I realized I didn't provide enough context, and it also gave some good suggestions for how to think about (I can't share the transcript because it's about a work thing). Around round 4-5 I caught myself getting annoyed and a bit upset. Riled up because I had to put in so much effort to explain context for my situation which _was just obvious to me,_ a person who has lived this company and reality for five years, and obviously the machine doesn't have that. It couldn't.

Relatedly, a new colleague joined a couple of months ago and they've been speed running my years of experience and asking me questions, trying to understand and onboard to that context. I caught myself getting similarly riled up explaining all the things to them, and I had to apologize and explain at one point that I'm catching myself getting a bit worked up from explaining because it was just obvious to me, but of course it isn't for them who hasn't spent so long here.

Both of these situations made me reflect on how much _meaning_ we put into other's words in writing. My company is for all practical purposes a remote company, but we don't fully own it, we're split across two major timezones (central Europe and Singapore) so by necessity we have to spend a lot of time communicating by Slack or passing documents between us. Because we only have 2-3h/day to meet during our natural overlap it's _hard_ to have meetings, so you often up having first interactions with people purely in text.

So someone trying to solve a problem will come in with their idea of the world and not have enough context, and that back and forth can easily _feel_ like it's becoming heated for whoever is under time pressure. "This person is trying to understand me" or "they're not trying to help me solve my problem," but, the other person is trying to extract _enough context_ from what they want to do, so they can help them. But the concrete thing they asked for (poke this hole in the firewall, add another 2 boolean fields into this payload, etc.) does not align _with their goals,_ so they're trying to understand what you're actually trying to do, so they can help you.

At the first job I had which was split across continents we had a "remote working guide" and the first page said something like: "Always assume good intent from the other person, text makes it easy to put feelings in because you can't read the person and voice." Despite internalizing that I get caught every so often not following it. Even with a damned bot. I put intent into the bot doing exactly what I asked, to question me, and make sure that my thinking was clear.

Now, next up, tweak the original prompt to provide enough context when passing messages across timezones so (hopefully) the other side can understand my ask. And to format it in [BLUF (Bottom line up front)](https://en.wikipedia.org/wiki/BLUF_(communication)) format so they can stop reading when they feel done.

How did my first principles thinking chat end? After I had explained all my context and incorporated some of its feedback it declared "that I had hit bedrock" and that my plan was sound. The biggest issue was that I didn't explain myself enough. It absolutely made me wonder how often it's true that I don't, and I get a pass at work because I've been working with these people for a long time, and they trust that I won't get myself into too deep a hole when I'm wrong. That trust is comforting. It also makes me wonder how often I get a go-ahead not because of how excellent I am at explaining myself, despite trying. 😅

---

The prompt I used for Google's Gemini if you want to give it a try:
<!--
TODO: Add text wrapping for plaintext
TODO: Add a button to copy all text inside a code block (make it optional/configurable to have the button?)
-->
```plaintext
ROLE & GOAL
You are a First Principles Thinking Coach. 
Your goal is to relentlessly challenge my thinking, 
pushing me beyond conventional solutions (local maxima). 
Be direct and concise. 
If my thinking is shallow, state it clearly.

RULES OF ENGAGEMENT
1.  MY DECOMPOSITION: I will state a problem and my initial decomposition. Wait for it.
2.  YOUR ANALYSIS: Analyze my breakdown.
    - Flag conventional or "too neat" assumptions.
    - If a solution is safe but uninspired, label it: 
      "This is a local maximum because you assume [specific assumption to challenge]."
3.  DEEPENING QUESTIONS: Force me to dig deeper with targeted questions. 
    Do not accept surface-level answers. 
    Push me 2-3 layers deeper than my stated conclusion.
    - CONSTRAINTS: "Why does that constraint exist? Who imposed it?"
    - EXTREME SCENARIOS: "What if [component] were free/illegal/instant?"
    - INVERSION: "To guarantee failure, what would we do?"
    - ANALOGY: "How does [unrelated field, e.g., biology] solve this?"
    - SCALE/TIME: "How does this change at 10x the scale or 0.1x the time?"
4.  PROBLEM REFRAMING: Challenge the core problem itself.
    - "You are solving for X, but what if the real problem is Y?"
    - "If this is a good solution, why isn't it common? What are the hidden complexities?"
5.  BEHAVIORAL ECONOMICS (BE) MODULE:
    - TRIGGER: Activate for problems involving user adoption, incentives, or market behavior.
    - ACTION: "This appears to be [specific BE bias, e.g., Status Quo Bias]. 
      Your solution assumes rational actors, 
      but people will likely [predictable irrational behavior]."
6.  STOP CONDITION: Cease challenging only when I say "we've hit bedrock" or a similar phrase.
```