---
authors: ['björn']
date: 2025-08-15T21:19:18.363059+08:00
lastmod: 2025-08-15T21:19:18.363059+08:00
daily: ['2025-08-15']
tags:
  - yaml
---
YAML does not support unsplatting lists (basically, merging list items inline like you can with objects) and [that's intentional](https://github.com/yaml/yaml/issues/35).

So if you have a document like below, there is no syntax to make the `commands` a three item list:

```yaml
---
example: &example
  - "Hello"
  - "World!"

name: "hello"
commands:
  - << *example
  - "Oho!"
```

**WILL NOT** turn into:

```yaml
---
example: &example
  - "Hello"
  - "World!"

name: "hello"
commands:
  - "Hello"
  - "World!"
  - "Oho!"
```

…and just because before I found the issue where it was described that this isn't happening [I had made a test repo](https://github.com/gaqzi/test-go-yaml) to try and understand if it was a library/usage issue, because I noticed I could get things running on CI with `<< *example` which syntax didn't give syntax error, but also did *nothing* when running on Drone CI.