---
author: björn
comments: true
date: 2022-02-05 16:30:00 +08:00
layout: post
slug: sticky-blocks-in-roam-research
title: Sticky blocks in Roam
subtitle: floating along in your sidebar
description: >
  I use Roam Research to think and manage my tasks, and I wanted a way to
  make blocks float along in the sidebar, so I can quickly organize my task 
  list.
categories:
- blog
tags:
- css
- roam research
- workflow
---
I use [Roam Research] as my primary way of thinking and keeping track of
tasks. My current workflow has me creating a list of all tasks I want
to get done, and then I drag them to either `Done` or some follow-up/waiting
area for future action. So I only see things I can act on now.

My list of things to action can get quite long, and when I'm processing
follow-up items, I would have a hard time dragging them to `Done` because it
was too far away in the sidebar. So I wished I would make the `Done` float
with me, so I could always have a quick way of pulling it there.

While looking at the custom styling in the [Roam Book Club] graph, I found
the `#sticky` tag, which will make a block sticky over the children in the
block. So I took that CSS and modified it slightly to support making a
block float, so I could have it stay with me in the sidebar.

An example of how it looks in my sidebar before my new tags:
{% img alt="Unmodified list" /img/2022/02/05/01-bare-listing.png %}

With the `#sticky` tag from the Roam Book Club, I can make for example
`Tasks` float when I'm scrolling inside the tasks. This can be super helpful
for keeping track of where you are (they use it for daily chat pages) but
not quite what I need:
{% img alt="#sticky" /img/2022/02/05/02-sticky.png %}

Introducing `#sticky-block`, which will make the block and all its children
float along at the top of the page, so I can always drag things there quickly:
{% img alt="#sticky-block" /img/2022/02/05/03-sticky-block.png %}

```css
/* To make blocks float, a constant in the sidebar */
.roam-block-container[data-page-links*="sticky-block"]
/* To make the a block float over its children. 
   So you see which block you're currently inside.  
   The weird \" is because it would match both sticky and stick-block and   
   double up the rendering. 
   */
, .roam-block-container[data-page-links*="sticky\""] > .rm-block-main
 {
  position: sticky;
  top: 0;
  z-index: 11;
  background: white; /* Might have to be adjusted for your theme */
  padding-top: 4px;
  padding-bottom: 2px;
  margin-bottom: 10px;
  box-shadow: 
    0 1px 1px rgba(0, 0, 0, 0.034), 
    0 1px 1px rgba(0, 0, 0, 0.048), 
    0 12.5px 10px rgba(0, 0, 0, 0.06), 
    0 12.3px 7.9px rgba(0, 0, 0, 0.072), 
    0 7.8px 10.4px rgba(0, 0, 0, 0.086), 
    0 5px 120px rgba(0, 0, 0, 0.12);
}

/* Hides the tag since it's not important in the output, and there is 
special styling so it's clear that something extra is going on. */
span.rm-page-ref[data-tag="sticky-block"],
span.rm-page-ref[data-tag="sticky"] {
    display: none;
}
```

**Note:** This CSS currently does not support having both `#stick-block` and 
`#sticky` for the same page, they will overlap each other, and the second 
element will block the first. I don't currently need this, so I haven't spent 
the time. :) 

[Roam Research]: https://roamresearch.com/
[Roam Book Club]: https://twitter.com/RoamBookClub
