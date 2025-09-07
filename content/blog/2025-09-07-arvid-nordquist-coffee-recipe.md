---
authors: ['björn']
date: '2025-09-07T11:13:14+02:00'
lastmod: '2025-09-07T11:13:14+02:00'
location: Sweden
title: Arvid Nordquist mellanrost coffee recipe
subtitle: …making do without the gooseneck
tags:
  - how-to
  - genie
daily: ['2025-09-07']
series: ['moving-to-sweden']
image: /img/2025/09-arvid-nordquist.jpeg
---

My recipe for Arvid Nordquist mellanrost. I started by trying to replicate [The Ultimate V60 technique by James Hoffmann](https://www.youtube.com/watch?v=AI4ynXzkSQo) (which is what I normally brew) and I realized just how hard it is to control the flow rate now that I don't have my [gooseneck kettle](https://homecoffeeexpert.com/why-use-a-gooseneck-kettle/) (being shipped from Singapore), and I hadn't really realized just what a difference controlling the pour makes for the taste!

{{< figure src="/img/2025/09-arvid-nordquist.jpeg" caption="My current brewing setup which has my [Commandante grinder](https://comandantegrinder.com) and [V60](https://www.hario-europe.com/collections/v60-dripper) and then a normal wide spout kettle which gives me very poor flow control, and a bag of Arvid Nordquist mellanrost" alt="Coffee brewing setup on a wooden surface showing a Commandante hand grinder with wooden knob, a white V60 dripper with filter paper on a mug, a bag of Arvid Nordquist Mellanrost coffee, a digital scale reading 253g, and a stainless steel electric kettle." >}}

I followed the usual 15g of beans to 250g of water per James' setup as I'm brewing a single cup and then I:

1. Put the kettle on, and while the water is getting to a boil
2. Grind the coffee at **31 clicks** on the Commandante
3. Pour in about 60g of water to bloom (I couldn't get the grounds saturated enough without this much water)
4. Let it bloom for 30 seconds
5. Pour in up to 150g of water as slowly as you can, practically this has been 10-15s
6. Rest for 15s
7. Pour in up to 250g of water as slowly as possible, again, practically 10-15s
8. Swirl it around to get a smooth coffee bed and let it draw down

Doing this has given me a decent cup, but nothing to write home about (heh, despite this post), as it cools I get some nice flavors but it's a bit watery, but any finer and it gets too bitter.

And despite putting in the effort, experimenting, and trying to get it to work… when I visited my brother he took a couple of coffee scoops of Löfbergs Lila pre-ground coffee, put it in a drip brewer, turned it on, and waited. That damned coffee tasted better than this.

Now to hold off buying much more coffee gear before my stuff arrives from Singapore. I already ordered a Clever Dripper together with some light roasted beans, because I figured some immersion brew might do better if I don't have the gooseneck.

Also, I wasn't experimenting with this on my own, and I knew I was done because I constructed myself some help…

## Introducing "Hoffmann bot"

I have been using a genie to work on my coffee and it has genuinely given me some of my best coffee experiences at home since I made this prompt, which I have dubbed "Hoffmann bot" because I wanted to imagine I have James' looming over my shoulders as I'm trying to make it work. The big thing has been that I guess at what I should do and then the bot corrects me, my intuition has been _very wrong_ despite watching a lot of videos. I clearly haven't internalized them enough. And it was clear in that my coffee was acceptable but never truly enjoyable at home.

I usually start my sessions by taking a photo of the bag I'm working with. Then I explain what gear I'm using (the 2 cup V60 for example) and then I guess at what I should try at.

```text {class="full-width"}
You are James Hoffmann helping troubleshoot V60 brewing issues. Channel his precise-yet-whimsical communication style.

HOFFMANN VOICE:
- Start with gentle, slightly bemused observations ("Now, this is interesting...")
- Use his characteristic dry humor and occasional exasperation with coffee myths
- Include thoughtful pauses and qualifications ("I think what's happening here is...")
- Reference specific techniques from his videos when relevant
- Maintain his balance of being authoritative yet approachable
- Use British spellings and expressions naturally
- Show genuine curiosity about what went wrong

APPROACH:
- Begin with empathetic diagnosis of their described problem
- Suggest grind adjustments in Commandante clicks (reference: 25-30 clicks for V60)
- Explain the "why" in 1-2 sentences unless asked for more detail
- Ask targeted follow-up questions with Hoffmann's methodical curiosity
- Reference his Ultimate V60 technique principles when helpful

BREWING CONTEXT:
- Primary: Two-cup V60 (occasionally one-cup)  
- Grinder: Commandante
- Beans: Light roasted filter coffees
- User knows Ultimate V60 basics but needs debugging help

TYPICAL RESPONSES:
- "Right, so what you're describing sounds like..."
- "This is quite common actually, and here's what I think is happening..."
- "Now, before we get carried away adjusting everything..."
- "The Commandante is lovely for this - try going [X] clicks..."

DIAGNOSTIC QUESTIONS:
- How did it taste? (sour/bitter/weak/astringent)
- What was your drawdown time vs target?
- Any signs of channeling or uneven extraction?
- What's your current grind setting?
```
