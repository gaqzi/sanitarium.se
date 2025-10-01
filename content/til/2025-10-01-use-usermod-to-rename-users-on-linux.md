---
authors: ['björn']
date: '2025-10-01T13:24:05+02:00'
lastmod: '2025-10-01T13:24:05+02:00'
location: Sweden
title: 'Use usermod to rename users on Linux'
tags:
  - linux
daily: ['2025-10-01']
series: []
---
Use `usermod -l newuser -d /home/newuser -m olduser` when renaming a user account, because it'll update all relevant system files and move the home folder in one go.

Then `groupmod -n newgroup oldgroup` if you need to rename the group.
<!--more-->

I had a vague memory of being able to change settings (shell etc.) by updating using `vipw` so I renamed there and then edited `/etc/groups` but I then got an error when trying to become that user:

```text {class="no-copy-button"} 
# su bjornnow
su: Authentication failure
```

To fix it, I had to update all these files (and rename the home folder):

- `vipw`: updates `/etc/passwd`
- `vipw -s`: updates `/etc/shadow` which contains the password hashes and are only readable by root
- `vigr`: updates `/etc/group`
- `vigr -s`: updates `/etc/gshadow` the same as passwd (also TIL, groups can have passwords)

This is what you get when you think you remember how things work, and didn't want to look up how usermod worked, a little bit of knowledge is dangerous and all… 😅
