---
authors: ['bjơrn']
date: 2025-08-15T21:19:18.362876+08:00
lastmod: 2025-08-15T21:19:18.362876+08:00
location: Singapore
title: Syntax for declaring and using YAML anchors
daily: ['2025-08-15']
tags:
  - yaml
---
The YAML anchors to name a reusable section are defined by `&name` and then to use them to replace the value of something you do `*name`, if you want to "unsplat"/merge a dictionary/object then use `<<: *name` and then it'll insert it at that point.

<!--more-->

```yaml
world: &world World
example: &example-anchor
  HELLO: *world
  There: Yo

my-values:
  <<: *example-anchor
  foo: bar
```

becomes

```yaml
---
example:
  HELLO: World
  There: Yo
my-values:
  HELLO: World
  There: Yo
  foo: bar
```
