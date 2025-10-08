---
authors: ['björn']
date: '2025-10-08T15:14:34+02:00'
lastmod: '2025-10-08T15:14:34+02:00'
location: Sweden
title: Hugo's resources.Get only finds files in assets/, not static/
tags:
  - hugo
daily: ['2025-10-08']
series: []
---
Hugo's `resources.Get` only finds files in `assets/`, not `static/`.

I kept my assets/resources in `static/` and didn't get why I always had to write `/absolute/urls` and use hope as a strategy, 
when I moved them into `assets/` I could look up all my assets.
<!--more-->

The below would fail because it couldn't find the asset:

```plain
{{ with resources.Get "/author/bjorn.jpg" }}
  <img src="{{ .RelPermalink }}" alt="Björn Andersson">
{{ end }}
```

Hugo has global assets accessed through `resources.Get` which **only** looks up in `assets/`.
Then page assets that you get through `.Page.Resources.Get` instead, which I haven't used yet.

If you want to use both, then do like the [figure shortcode](https://github.com/gohugoio/hugo/blob/4414ef73f3cd490caf93e0d50a6102db9ab28318/tpl/tplimpl/embedded/templates/_shortcodes/figure.html#L9C5-L11C16) and do it in an or:

```plain
{{- with or (.Page.Resources.Get $u.Path) 
            (resources.Get $u.Path) -}}
{{- $src = .RelPermalink -}}
{{- end -}}
```
