---
authors: ['björn']
date: 2025-08-02T09:37:29.210453+08:00
lastmod: 2025-08-02T09:37:29.210453+08:00
location: Singapore
daily: ['2025-08-02']
title: Link rel="canonical" is like a correlation ID
tags:
  - html
---
The `<link rel="canonical" href="…">` is a bit like a correlation ID between services and I need also to have it on my canonical page, because if someone sends it with `?utm_source=foo` it __could__ be a different page than the one without the query string.
