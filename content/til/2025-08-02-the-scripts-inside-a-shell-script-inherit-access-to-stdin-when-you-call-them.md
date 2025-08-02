---
author: 'björn'
date: 2025-08-02T09:37:29.209371+08:00
daily: ['2025-08-02']
lastmod: ''
tags:
  - shell-scripting
---
The scripts inside a shell script inherit access to STDIN when you call them, so if you have a shells script that only has `cat` and you do `./script.sh < script.sh` then it'll output the content of itself
