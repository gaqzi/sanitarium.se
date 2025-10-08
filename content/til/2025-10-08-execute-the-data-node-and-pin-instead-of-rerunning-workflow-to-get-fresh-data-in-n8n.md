---
authors: ['björn']
date: '2025-10-08T16:23:39+02:00'
lastmod: '2025-10-08T16:23:39+02:00'
location: Sweden
title: 'Execute the data node and pin instead of rerunning the workflow to get fresh data in n8n'
tags:
  - n8n
daily: ['2025-10-08']
series: []
image: /img/2025/10-n8n-step-rerun.png
---
{{< figure src="/img/2025/10-n8n-step-rerun.png" alt="n8n workflow showing a sequential workflow starting with RSS fetching and going through Telegram, Mastodon, and Bluesky" >}}

Execute the data node/step and pin it,
instead of rerunning the workflow or the step that relies on that data,
when modifying a step that needs fresh data.

Example: When modifying Mastodon/Bluesky cross-posting nodes that depend on an RSS Feed Trigger,
execute and pin the RSS node.
Then iterate on the posting logic that _only depends_ on the RSS data without triggering any posting.

<!--more-->

Where my confusion came from: I haven't figured out fan-out and fan-in,
because I would expect to run my cross-posting in parallel and not sequentially,
but… I have seen there _is_ some kind of fan-out, but how to use it? 🤷

So my assumption that I wouldn't get the data reloaded if I **only** ran the first step was incorrect,
and I've been a bit hesitant to test since there's only production (this personal stuff doesn't have a proper testing env 😅).
