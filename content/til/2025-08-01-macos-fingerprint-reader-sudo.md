---
authors: ['björn']
date: '2025-08-01 23:15:00+08:00'
lastmod: '2025-08-01 23:15:00+08:00'
location: Singapore
daily: ['2025-08-01']
title: Enabling macOS fingerprint reader for sudo
tags:
  - how-to
  - macos
---
You can enable the fingerprint reader for sudo on macOS,
and pressing my finger on a button beats having to type the password, steps:

1. `cp /etc/pam.d/sudo_local{.template,}` 
2. Edit `/etc/pam.d/sudo_local` and uncomment `auth       sufficient     pam_tid.so`. 

The reason for doing this in `sudo_local` is that this file will not get reset with system changes from Apple.
