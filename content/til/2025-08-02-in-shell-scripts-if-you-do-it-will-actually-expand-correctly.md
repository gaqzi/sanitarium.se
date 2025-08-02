---
author: 'björn'
date: 2025-08-02T09:37:29.209663+08:00
daily: ['2025-08-02']
lastmod: 2025-08-02T09:37:29.209663+08:00
tags:
  - shell-scripting
---
In shell scripts if you do `"$@"` it will actually expand "quoted sentences" correctly, and if you just do `$@` it will **always** unwrap them into single words, I thought that if you did `"$@"` it would combine all arguments into a single argument, and what it does is do what I thought `$@` alone did.
  
I.e., with `"$@"` the arguments `"one two" three` will be 2 arguments, the first being `"one two"`, and without it will become three arguments, all separated by space.
