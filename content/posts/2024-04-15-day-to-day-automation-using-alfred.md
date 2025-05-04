---

author: björn
comments: false
date: 2024-04-15T19:15:00+08:00
last_modified_at: 2024-04-16T12:30:00+08:00
layout: post
title: Day-to-day automation using Alfred on your Mac
subtitle: reducing TOIL outside of your DevOps practice
categories:
  - blog
tags:
  - toil
  - automation
  - alfredapp

---



I try to be aware of where I have friction in my day-to-day when working at my
computer, keeping an eye out for [TOIL to remove.][TOIL] Whether it's from
manually repeated actions, or from differing behaviors across apps and services
I use. When I identify any of these I try to spend some small amount of time
automating or changing how I work to improve.

All of these things don't necessarily make a lot of sense from how much time I
save, but, it also makes me happy to spend a bit of time improving my
environment, and spending a bit of time to make me happy is good enough for me.

I view doing these kinds of small workflow improvements like a [kata] because it
improves my automation/scripting skills and encourages me to think about how I
work. I usually give myself 10-20m to try and make these kinds of improvements
just so I know how much time to spend. Just don't go overboard. XKCD, as always,
have a comic to illustrate the downside of going too far. 🙂

[TOIL]: https://sre.google/sre-book/eliminating-toil/

[kata]: https://en.wikipedia.org/wiki/Kata#Outside_martial_arts

[!['Automating' comes from the roots 'auto-' meaning 'self-', and 'mating', meaning 'screwing'."](https://imgs.xkcd.com/comics/automation.png)](https://xkcd.com/1319)

## What is Alfred and why is it an app I'm focusing on?

[Alfred] is an application launcher but oh-so-much-more. It connects with macOS
and the Workflows contains a lot of extensions that allow you to interact with
all kinds of programs, websites, etc.

A big part of what Alfred has helped me create is a more unified experience
across the apps and websites I use. I have moved some operations that behave
differently in different apps into Alfred because then I can focus on what I
need to do and then use Alfred to provide consistency (and as I've
been told, "consistency is good even outside the bathroom").

Now, let's look at how I use Alfred.

[Alfred]: https://alfredapp.com/

## Built-in functionality

These are features that don't require anything extra to install and use.

### Open an app

Alfred's starter feature is the application launcher, and it means you summon it
with a keybinding and type the name of the app you want to start and voilà.
I have bound the keyboard shortcut to `cmd+space` and replaced the built-in
Spotlight search.

{{< img alt="Opening Firefox in Alfred" src="/img/2024/04/15/01-open-app.png" >}}

### Spell / define

There are certain words I rarely get right (continuous) and some
words are spelled very differently from how they sound. Summon Alfred and
`spell <word>` and you'll have suggestions that often will go right. And if
you don't find it, replace `spell` with `google` and see if Google knows
better. Hit enter to copy the correct spelling to the clipboard.

{{< img alt="Finding the correct spelling of continuus" src="/img/2024/04/15/02-spell-continuous.png" >}}

And `define` is the same thing but for dictionary lookup because you have some
word you're unsure what it means, or because you're wondering if someone was
trying to call you something you with some subtle nuance to a word. 😉
Hit enter to open the definition in macOS's dictionary app.

{{< img alt="Define 'laggard'" src="/img/2024/04/15/03-define-laggard.png" >}}

### Calculator

You can give it an expression and when you hit enter the result goes into the
clipboard. I often end up using this instead of opening a Python console on the
CLI.

{{< img alt="Adding some numbers together" src="/img/2024/04/15/04-calculator.png" >}}

### Custom web search

A custom web search allow you to quickly open a web browser at a
particular website with whatever value you've typed into Alfred which _doesn't
have to be a search engine or even a search page._

To configure a custom web search summon Alfred and hit `cmd+,` to open
the settings page. Go into the `Features` tab and click on `Web Search`.

{{< img alt="Alfred's setting Features -> Web Search highlighted" src="/img/2024/04/15/05-web-search-listing.png" >}}

Some example search engines I have made:

- Jira: `https://jira.example.com/browse/{query}`
  - This isn't a search but rather the view this ticket. Because I often get a
    ticket id (either from a commit message or someone rattling it off in a
    meeting) and this way I can open it quickly
- Confluence: `https://confluence.example.com/dosearchsite.action?
  queryString={query}`
- Wordnik: `https://wordnik.com/words/{query}`
  - So I can find synonyms and other alternatives for words. Often use this when
    I want to find a good name for something which has been inspired
    by [Hunting for great names in programming](https://signalvnoise.com/svn3/hunting-for-great-names-in-programming/).
- Pypi: `https://pypi.org/project/{query}`
  - To look up python packages

{{< img alt="Example setup of the Confluence search engine" src="/img/2024/04/15/06-web-search-example-config.png" >}}

## Working with other applications

Alfred has ended being the tool that brings my apps to focus and smoothes
over differences between apps.

### Give my most common apps a keybinding

Instead of `cmd+tab` between the various apps I'm using I have bound specific
keybindings to my most used app, so I can quickly swap between
them. [Hat tip to Rico Sta. Cruz](https://dev.to/rstacruz/switching-apps-slow-down-my-productivity-and-how-i-fixed-it-2anb)
who blogged about this a couple of years ago and who I picked it up from.

The big benefit I have found here is just the ease of being mid-thinking and
wanting to switch back to another app, whether it's to jot down a quick note, to
finish that Regex you were visualizing on [Regex 101](https://regex101.com/), or
to get back to Slack to paste that thing your colleague asked for. It feels so
seamless compared to tabbing between.

This is using [Alfred's Workflows](https://www.alfredapp.com/workflows/), and
they're part of their advanced set of options. You can do keybindings that work
across all of macOS as well as actions based on what you're typing.

{{< img alt="The custom app shortcuts workflow" src="/img/2024/04/15/07-app-shortcuts.png" >}}

### Spotify controller

I have been using these keybindings since before Alfred, in Quicksilver, and
there are other workflows for Spotify but since I had these I never bothered
installing anything else.

The cool extra in this workflow is that I added a keyword to open the
current playing song on [Genius.com](https://genius.com) because I like
reading the lyrics.

This is an example of something where the automation is _far from necessary,_
but, I enjoyed adding it. It's something I do every other week and knowing I
can just go straight into the song nearly every time is great.

{{< img alt="Spotify keybinding and keyword configuration" src="/img/2024/04/15/08-spotify-keybindings.png" >}}

My [Spotify workflow] is on Github if you want to install it, or [here's a gist]
if you're just curious how I made "open on genius."

[Spotify workflow]: https://github.com/gaqzi/alfred-workflows/blob/master/Spotify%20keyboard%20shortcuts.alfredworkflow

[here's a gist]: https://gist.github.com/gaqzi/b3de88050bf1caaf8d2661233b51a1ae

### Global microphone mute/unmute shortcuts

I regularly use Google Meet, Slack, and Zoom for talking with people, and these
apps all use different shortcuts to mute. So instead of keeping the app
focused and remembering the various shortcuts I now just leave myself unmuted
everywhere and directly mute/unmute the OS through Alfred. My mic has a visual
indicator when it's on. +I have a notification posted, so I can see the current
status on the screen.

As I started using this workflow I realized that sometimes the microphone
bugs out but swapping it between the built-in and back will fix it. So after
a while I made a script to help swap as well.

And finally, I realized that sometimes my virtual soundcard which removes
background noise ([krisp.ai](https://krisp.ai)) hangs and needs to be
restarted, so another keybinding to quickly restart the soundcard.

The only downside of this workflow is that others can't as clearly see when
I want to speak by unmuting myself in the current app, so in those rare cases
I'll use the mute in the app itself. Because optimizing my workflow
shouldn't come at the pain of everyone else, we live in a society. 🙂

{{< img alt="The mic switch workflow setup" src="/img/2024/04/15/09-mic-switch.png" >}}

This [mute/unmute workflow] is available on Github,
and [here's a gist][mute-gist] if you want to see the toggle code. My
dotfiles got the [swap mic script] and the [restart krisp script].

[mute/unmute workflow]: https://github.com/gaqzi/alfred-workflows/blob/master/Toggle%20mute%20mic.alfredworkflow

[mute-gist]: https://gist.github.com/gaqzi/f299047706c10b2616ba15c94cabf1fe

[swap mic script]: https://github.com/gaqzi/conf/blob/master/bin/swap-mic-input

[restart krisp script]: https://github.com/gaqzi/conf/blob/master/bin/%2Crestart-krisp

## Improvement to my day-to-day workflow

### Text replacement / snippets

Snippets are short pieces of text that expand into something else. It can be
a static string, or it can be dynamic and I use both kinds as I work. For me
they fall into these categories

1. "Named paste", things that are hard to remember or unwieldy and are now not
2. Dynamic replacement, something that follows a pattern and I want to swap
   between. Generally these use the clipboard
3. Generated inputs, I need the current time in a specific format or some
   other piece of data

You configure snippets by summoning Alfred and hitting `cmd+,` which opens
Settings, then go into Features -> Snippets. Snippets work by specifying a
keyword, in my default bundle I require that my keywords are prefixed with `\\`,
meaning that Alfred will expand my snippets if it sees `\\<keyword>` and with
the example keyword `exp` you'd then type `\\exp` to add it. If you need to type
the exact string for some reason it's easiest to add a space somewhere before
you type the last character and then go back and remove it.

{{< img alt="How to view or create snippets" src="/img/2024/04/15/11-snippets-config.png" >}}

My trigger for creating a snippet is finding that I keep typing or
pasting the same thing again and again.

Let's look at how I use them in a couple of different places.

#### GMail

Finding emails from "unusual senders:" I label the majority of emails I get
at work as they are notifications or otherwise automated emails. So if I get
something that isn't labeled it's probably a human or something I need to
look into, and it can sometimes get hidden in a sea of everything else.

`<prefix>gmailn` in the search bar turns into `is:inbox is:unread
has:nouserlabels` which only shows unread emails in the inbox which doesn't
have a label.

When I'm processing my labels, which are effectively buckets of things to do,
I often go into a label and want to see only the unread items, so I can open
the first and then go through them one-by-one. So open the label, focus on
the search bar, and type in `<prefix>unr` to give me `is:unread` and then
get to that focus.

#### Jira tickets

If I'm writing a message on Slack and I need to reference a ticket I think
it's nice to give a link even if I only have the jira ticket ID, so I made a
snippet that adds the current clipboard item at the end of my company's Jira
instance in a Markdown link. Now it looks nice where markdown is and the
other person doesn't have to open it up themselves.

Copy `WRK-123` and then type `<prefix>jiramd` which replaces it with
`[WRK-123](https://jira.deliveryhero.com/browse/WRK-123)`.

The Alfred snippet configuration
```
[{clipboard:trim}](https://jira.example.com/browse/{clipboard:trim})
```

{{< img alt="Configuring the jiramd snippet in Alfred" src="/img/2024/04/15/12-snippet-jiramd.png" >}}

#### Roam Research

Roam is my notetaking app and where most of my thinking happen and I have a
whole slew of replacements for how I work with Roam Research and most of them
are to help me keep my workflow consistent (using the right tags)
and to make common actions easier and faster.

- `<prefix>rts` turns into the current time in bold since I practice
  interstitial journaling. Example `**15:03**`. Snippet configuration: `**
  {time:short}**`
- `<prefix>b<shortcode>` for how I bucket tasks so when I spend time on a
  particular bucket I can find the things I need to do. I.e. my bucket  "Life in
  Production" (on-call, observability, continuous delivery, etc.) is prefixed
  with `<prefix>bl` and that turns into `[🥬]([[Bucket/Life in Production]])`
- `<prefix><INITIALS>` to turn into the name of my most frequent
  collaborators at work, so I can tag what I've said to them or a task we
  need to do.

### Emoji search

Spending a lot of time communicating across continents involves timezones
and people rarely hearing your voice, so I have gotten used to peppering my
inputs with emojis to help since it's so easy to come off sounding like an
ass otherwise.

And because some websites or applications don't have a good search for
emoji and this way I only have to learn one keyboard shortcut and normalize it
across places. This way I don't have to remember how Slack named this emoji vs.
Miro vs. Google Docs vs. Confluence vs. other random website. I just learn it in
Alfred and then paste it straight into the textbox I wanted.

{{< img alt="Searching for the rocket emoji" src="/img/2024/04/15/10-search-emoji.png" >}}

This is an external Workflow made by [James Sumners], and you can download it
from the [workflow's Github page.](https://github.com/jsumners/alfred-emoji)

[James Sumners]: https://github.com/jsumners

### Generate uuids on the fly

As I was writing the tying it up section I realized that I had a recent pain
which where I kept jumping between apps to create new UUIDs. I was running
the following command on the CLI and then pasting it into some yaml files in
my editor.

```shell
uuidgen | tr '[:upper:]' '[:lower:]' | tr -d '\n' | pbcopy
```

So I instead created a new workflow that is triggered by a snippet that runs
this for me.

{{< img alt="Configuring the uuidgen snippet" src="/img/2024/04/15/15-snippet-uuidgen.png" >}}

**Note:** To make it behave just like a regular snippet you need to
configure the _Copy to clipboard_ output to `Automatically paste to the
frontmost app` and `Mark item as transient in clipboard`.

{{< img alt="How configure the Copy to clipboard output" src="/img/2024/04/15/16-snippet-uuidgen-clipboard-config.png" >}}

The [uuidgen workflow] is available on Github.

[uuidgen workflow]: https://github.com/gaqzi/alfred-workflows/blob/master/uuidgen.alfredworkflow

## Other workflows

Some other workflows I have installed since they save me time.

### Calculate Anything

I installed this for two reasons: to quickly translate cooking recipes using
imperial units into metric and currency conversion. Super convenient and now I
can finally get how much 16 floz is in ml (473.176) without needing to go
online.

{{< img alt="Calculate Anything converting 16 floz to ml" src="/img/2024/04/15/13-calculate-anything.png" >}}

By [Biati Digital] and available in
the [Alfred Gallery](https://alfred.app/workflows/biatidigital/calculate-anything/).

[Biati Digital]: https://github.com/biati-digital

### Epoch converter

There was a time when I kept looking at unix timestamps and needed to quickly
get when it was, so copying and then `ts <paste>` gave me when it was and
`ts` without anything will give you the current unix timestamp.

{{< img alt="Epoch Converter showing the current unix timestamp" src="/img/2024/04/15/14-epoch-converter.png" >}}

By [Julien Lehuen] and available in
the [Alfred Gallery](https://alfred.app/workflows/julienlehuen/epoch-converter/).

[Julien Lehuen]: https://github.com/snooze92

## Tying it up and how I figure out what to add

I hope the above gives you some ideas or inspiration for what you could do
to improve your day-to-day computer usage. These are things that I've pulled
together over years, and similarly I have a [bin/ folder] with other types of
automation I've accrued, hehe. 😅

[bin/ folder]: https://github.com/gaqzi/conf

Now, how have I accrued these things? I generally try to reflect on the work
I do and the biggest help to it has been scheduling 30min every Friday to
reflect on the week. This session covers everything from updating my [brag
document] to reflecting on what work I felt I repeated a lot and whether
there's anything there to spend time on in the future. Pretty much,
what annoyed me when working and can I do something about it?

If I come up with something that I can't deal with right now then I'll
record it in Roam under `#hack-idea`, whether it's Friday or not, and when I
feel like hacking on something I'll look there. Because sometimes you just
need something quick to hack on. 🙂

I'd love to hear what your favorite day-to-day automations are
on [Mastodon](https://hachyderm.io/@gaqzi)!

[brag document]: https://jvns.ca/blog/brag-documents/
