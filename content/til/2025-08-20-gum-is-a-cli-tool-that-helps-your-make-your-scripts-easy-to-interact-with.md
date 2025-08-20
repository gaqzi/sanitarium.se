---
authors: ['björn']
date: '2025-08-20T23:02:03+08:00'
lastmod: '2025-08-20T23:02:03+08:00'
title: 'gum: clean user interactions for shell scripts'
tags:
  - shell-scripting
  - gum
  - golang
daily: ['2025-08-20']
---
[gum](https://github.com/charmbracelet/gum) simplifies making shell scripts interactive: no more wrestling with read commands and ANSI escape codes for user input: just proper text editing, defaults, and clean UI.

Their demo: {{< img src="/img/2025/gum-demo.gif" alt="gum gemo" >}}

For example, if you run:

```shell
gum input --width 50 --header "Favorite author?" \
 --value "Terry Pratchett"
```

It will give you a question with a sensible default that you can then change as you want, and what you wrote as you hit `enter` will be returned so your script can then use it.

If you instead has some options where you want to select one:

```shell
gum choose --header "Favorite book?" \
 "Hogfather" "Thief of Time" "The Night Watch" "Small Gods"
```

Which gives you a selection box, you can configure to allow multiple selections, and the one you pick is then returned.

And one I really love, have it show a spinner to indicate that yes… something is still going on:

```shell
gum spin --title="Counting down from 10" sleep 10
```

Built on [bubbletea](https://github.com/charmbracelet/bubbletea), a Go TUI framework, use that directly if you need these components in Go code rather than shell scripts.