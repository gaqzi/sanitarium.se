---
authors: ['björn']
date: '2025-10-08T23:34:03+02:00'
lastmod: '2025-10-09T10:13:00+02:00'
location: Sweden
title: The regex | (or) operator splits the pattern left or right unless explicitly grouped
tags:
  - how-to
  - regex
  - background-work
daily: ['2025-10-08']
series: []
---
The regex `|` (or) operator splits the pattern left or right unless explicitly grouped.
Group it using `(pattern)` if you need to use the match later,
or as a non-capturing group `(?:pattern)` if you do it for clarity.

I used to think there was some magic rule about how `|` decided where to split,
but it's simply: characters and subpatterns concatenate into a single pattern first,
then `|` splits the entire thing left and right unless you explicitly group it.
That's because `|` [has the lowest precedence][precedence] so _all other_ operations happen first.

So while I used to think that `prefix_cat|dog` would match `prefix_cat` and `prefix_dog`,
it actually matches `prefix_cat` and then `dog`.

And that exact problem in a real-world example, to find if a page is linking to another, both relative or full URL:

[precedence]: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap09.html#tag_09_04_08

<!--more-->

The regex `<a[^>]+href=["']https://www.example.com/page|/page` will match `/page`,
just as in the `dog` example, it's splitting the whole pattern and isn't what I want.

See it in action with [the excellent Regex101.com](https://regex101.com/r/6RylLz/2):

{{< figure src="/img/2025/10-regex-01.png" alt="The Regex101.com site showing the Regex in action and that it matches /page" >}}

To make it do what I want I need to constrain it in a capturing group `(pattern)`,
and since I don't want to reference the group later,
I constrain it inside a non-capturing group `(?:pattern)`.

That gives me the pattern `<a[^>]+href=["'](?:https://www\.example\.com/page|/page)`,
and [then it matches](https://regex101.com/r/kgeGyp/3) both the full URL (https://www.example.com/page) and the relative URL (/page):

{{< figure src="/img/2025/10-regex-02.png" alt="The Regex101.com site showing the Regex in action and that it matches both links per the pattern as I intended" >}}

I love Regex101.com. 🙂
I have commented gnarly regexes in my code with links to it,
so colleagues can paste them there and understand what's going on.
The sidebar explains what each subpattern does,
and the color highlighting shows what matches what in real-time. 
