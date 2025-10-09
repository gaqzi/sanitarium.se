---
authors: ['björn']
date: '2025-10-09T11:50:33+02:00'
lastmod: '2025-10-09T11:50:33+02:00'
location: Sweden
title: Don't quote regex patterns in Bash [[ ]] tests, because they'll match literally
tags:
  - bash
  - regex
  - shell-scripting
daily: ['2025-10-09']
series: []
---
Don't quote regex patterns in Bash `[[ ]]` [tests], because they'll match literally.

So the below won't match because it's looking for a literal `$` in the string,
instead of matching at the end of the string:

```shell
file="https://example.com/blog-post/index.html"
[[ "$file" =~ "/index.html$" ]] && echo MATCH
```

But this will:

```shell
file="https://example.com/blog-post/index.html"
[[ "$file" =~ /index\.html$ ]] && echo MATCH
```

**Note:** `[[ ]]` is a Bash extension of the test command that supports regexes (among other things).
The `[ ]` is the POSIX standard test (see `man test`),
so `[[ ]]` features may not work in other shells or in limited shells like ash or sh.

I learned this while removing `index.html` from file paths to bust Cloudflare's cache for directory listings/pretty URLs.
I then used [parameter expansion] to replace the match with an empty string, so directory URLs are also purged:

```shell
echo ${file/index.html/}
```

[tests]: https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html#index-_005b_005b
[parameter expansion]: https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
