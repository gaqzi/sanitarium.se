---
authors: ['björn']
date: '2025-09-30T13:09:33+02:00'
lastmod: '2025-09-30T13:09:33+02:00'
location: Sweden
title: 'Use :focus-visible instead of :focus, because it will only show when helpful'
tags:
  - css
daily: ['2025-09-30']
series: []
---
Use `:focus-visible` instead of `:focus`, because it will [only show when helpful.][MDN]

`:focus-visible` only shows focus styling when the browser determines keyboard navigation is being used, unlike `:focus` which triggers on all interactions including mouse clicks.

<!--more-->

```css
button:focus-visible { outline: 2px solid blue; }
```

This prevents the "clicked button stays highlighted" problem while preserving accessibility for keyboard users. [Full browser logic on MDN][MDN].

[MDN]: https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible#focus_vs_focus-visible
