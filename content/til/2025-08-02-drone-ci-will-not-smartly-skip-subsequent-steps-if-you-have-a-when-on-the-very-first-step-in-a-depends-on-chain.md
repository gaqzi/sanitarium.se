---
authors: ['björn']
date: 2025-08-02T09:37:29.210320+08:00
daily: ['2025-08-02']
lastmod: 2025-08-02T09:37:29.210320+08:00
title: Drone CI's DAG ignores skipped steps
tags:
  - drone-ci
---
Drone CI will **not** smartly skip subsequent steps if you have a `when` on the very first step in a `depends_on` chain, so you have to repeat the `when` condition for each step because it doesn't realize that the first dependency is gone.
