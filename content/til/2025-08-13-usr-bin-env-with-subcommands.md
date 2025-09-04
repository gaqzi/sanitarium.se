---
authors: ['björn']
date: '2025-08-13T08:21:23+08:00'
lastmod: '2025-08-13T08:21:23+08:00'
location: Singapore
title: '/usr/bin/env handles commands with subcommands'
tags:
  - shell-scripting
daily: ['2025-08-13']
---
`/usr/bin/env` executes commands with flags/subcommands, not just bare executables. Which is great if you, for example, have a `script/lint` that's a Python script, and it needs dependencies from a virtualenv that isn't active when you call it.

Just put your shebang as `/usr/bin/env uv run python3` and it always runs in the virtualenv, no wrapper script needed. This feels obvious in hindsight, it's _what you expect_ from these tools 😃

