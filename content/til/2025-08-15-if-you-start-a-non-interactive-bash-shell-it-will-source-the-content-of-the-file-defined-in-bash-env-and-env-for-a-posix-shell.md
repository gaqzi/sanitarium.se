---
authors: ['björn']
date: 2025-08-15T21:19:18.362542+08:00
lastmod: 2025-08-15T21:19:18.362542+08:00
daily: ['2025-08-15']
tags:
  - shell-scripting
---
If you start a non-interactive bash shell it will source the content of the file defined in `BASH_ENV` (and `ENV` for a POSIX shell).

> When bash is started non-interactively, to run a shell script, for example, it looks for the variable `BASH_ENV` in the environment, expands its value if it appears there, and uses the expanded value as the name of a file to read and execute.  Bash behaves as if the following command were executed:
>
>   `if [ -n "$BASH_ENV" ]; then . "$BASH_ENV"; fi`
>
> but the value of the `PATH` variable is not used to search for the file name.
