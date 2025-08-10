---
authors: ['björn']
date: 2025-08-02T09:37:29.210190+08:00
daily: ['2025-08-02']
lastmod: 2025-08-02T09:37:29.210190+08:00
title: Drone CI's when targets the merge target for PR events
tags:
  - drone-ci
---
Drone CI's `when` for deciding in which cases to run steps/pipelines [targets](https://docs.drone.io/pipeline/docker/syntax/conditions/#by-branch) the __merge target__ branch for PRs and not the actual PR's, also it pulls from `refs/pull/<num>/head` instead of `refs/heads/<branch>` so you can't target the branch itself using the `pull_request` event (use `push` on the pipeline and then `branch` for the step instead).
