---
authors: ['björn']
date: '2025-08-24T10:40:00+08:00'
lastmod: '2025-08-24T10:40:00+08:00'
title: Angry at the genie
subtitle: …getting exactly what I wished for, eventually
tags:
  - thinking-out-loud
  - genie
  - learning
series: ['learning-with-genies']
daily: ['2025-08-24']
---

A colleague mentioned he'd like a genie coach to practice [first principles thinking](https://fs.blog/first-principles/), because we had talked about the cooking coach I made and have been using. So I decided to give it a try, whipped up a prompt, and gave it a spin.

I had a problem I'd been working on and wanted to see if there was another way of thinking about it. I also asked it to add [behavioral economics](https://en.wikipedia.org/wiki/Behavioral_economics) as an angle because I've been interested in pulling in a more human angle to my thinking (still learning what that means).

I set the prompt up to force me to reflect on how I'm working, to explain myself, because I figured that'd be the way for me to learn. So we started. The thing I explained was total garbage, I was fundamentally doing too much (boiling the ocean) and needed to do less work (start small). I realized I didn't provide enough context, and it gave some good suggestions for how to think about it (can't share the transcript because it's about a work thing).

Around round 4-5, I caught myself getting annoyed and a bit upset. Riled up. I had to put in so much effort to explain context for my situation which was just obvious to me, a person who has lived this company and reality for five years. Obviously the machine doesn't have that. It couldn't.

But the bot was doing **exactly what I asked it to do:** Question me. Push me to explain my thinking. Make sure my foundations were solid. I was getting angry at a genie for granting my wish perfectly.

How did my first principles thinking chat end? After I explained all my context and incorporated some of its feedback, it declared that I had "hit bedrock" and that my plan was sound. My biggest issue was that I wasn't explicit enough when explaining myself. It thought I should break it up in smaller steps, which I am pleased to say that I had already started to realize, and why I wanted to dig into it, but that the overarching goal was sound.  
…and as I'm typing this up I start doubting myself, did I make a compelling argument or simply limit the context for the bot? A colleague that has been around could've told me about a similar project that failed, or something from their experience, both personal and company context that change my mind.

It absolutely made me wonder how often that happens. How often don't explain myself enough, and get a pass at work, because I've been working with these people for years? They trust that I won't get myself into too deep a hole when I'm wrong. That trust is comforting. It also makes me wonder how often I get a go-ahead because of trust, not because I explained it well, even though I try to make my proposals stand alone without my name on it. 😅

The genie did exactly what I wished for. I just didn't realize explaining context _was_ the wish.

---

**Related:** At least humans are better at this, right? This directly led me to [reasonable assumptions ...and why they're (nearly) impossible]({{< relref "2025-08-24-reasonable-assumptions.md" >}}).

---

The prompt I used for Google's Gemini if you want to give it a try:

```text {class="full-width"}
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
