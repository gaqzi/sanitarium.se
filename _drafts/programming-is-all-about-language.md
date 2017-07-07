---
author: björn
comments: true
date: 2016-01-08 20:00:00 +08:00
layout: post
slug: programming-is-all-about-language
title: Programming is all about language
subtitle: And you should make it your own
categories:
- blog
tags:
- rant
- programming
- opinion

definitions:
  axiom: >
    An axiom is a self-evident truth which is taken for granted as the basis 
    of reasoning.
  lagom: >
    A Swedish word meaning 'just the right amount'.
---
# Background

I've been working with a friend on a project and we're finding that we have
some differences of opinion when it comes to how code should be structured and
made. In particular when it comes down to test code.

This is my try at making a point of why removing duplication, even in tests,
is a good thing.

Programming is about finding patterns and naming them. Like going looking for
new species of sharks, but not quite as dangerous.

# Your language

The things we're using to control our computers are called languages, because
they're functionally the same to the computer as English is to you and me.

Explanations are derived from sentences, which are made up of words. Each word
carries a meaning and "bigger" words can generally be explained by multiple
"smaller" ones. Take for instance the word {{ 'axiom'|define }}. The very first
time you see it in a text it might not make sense. But if you look up the
definition you'll know how it's used. And sometimes the gist of a word makes
sense from the context.

I think code is a lot like that, and most importantly, that we should be
writing code with the intention of expanding the vocabulary of the problem
until it's composed of {{ 'lagom'|define }} chunks.

In essence programming is about finding patterns and naming them. Like going
looking for new species of sharks, but not quite as dangerous.

## Frameworks

A language around a problem domain is usually called a framework.
For dealing with the web you can use [Django], which deals with a lot of the
plumbing involved in making a modern website.

Web frameworks originated in the world of [CGI] scripts where you had to handle
everything yourself. You still can. But trust me, it gets boring fast. Instead
of doing all the steps involved in an HTTP request for every endpoint you'll
invest your time in learning a framework like Django.

To use that proper you'll be spending time understanding not just how HTTP
works but also how Django works. But despite learning two things, and at that
Django's very specific vocabulary, you'll be better off in the long run.

# The point of contention

What me and my friend have been disagreeing about is how to write tests.
Especially just how much of the current state needs to be visible in each test.

For example lets take some tests I wrote for a custom [Splunk] command. I'm not
arguing that this code is perfect. But I'm very satisfied with it. It has a
whole bunch of helpers working together and each individual test can focus on
it's own definition, instead of the *how* of running the code under test.
Or how it was setup.

```python
pass  # Add the splunk test code
```

My friend finds that this code is hard to follow. By looking at the test
definitions he says he can't understand what is actually being tested. And the
best thing I could get as an explanation of what he would do to make it more
readable is inlining the `_run_command` since that would make it clear what I'm
testing. Because all the moving parts would be immediately visible.

My argument is that the whole test class is one context. I'm testing one thing,
and since the setup is basically the same between all tests (barring some
variables) it makes sense to encapsulate and name that pattern. A new word. The
language of the context "this custom splunk command" has grown to include
`_run_command`.

I assume that `_run_command` does what it says when called. Therefore I can at
a glance see: "I've given this input, this should've been the output". Looking
at my tests it's easy at a glance to see what is different. Setup and
assertion, two statements on average.

The cognitive load of my following along with my tests have been reduced. By
encapsulating the dreary details of how I'm running the command, and exposing a
minimal interface, I can spend less time thinking about what's going on. To me
this is basically a way to cache what's going on.

If I were to repeat this over and over it would be a bit like removing a
manhole cover on a street. As long as you're paying attention to where you're
going you'll be fine. But is that the kind of worry you should have to deal
with walking down the street?

# Conclusion

The point I'm making shouldn't be very controversial: Your test code is also 
code. Find patterns, bag and tag 'em. That is: extract into methods.

When encapsulation work well it's like talking with someone you trust. Because
you don't have to verify that everything they claim is true. And if you trust
the people that wrote the following code, would you then rather inline that
functionality?

```python
with self._successful_post_request(path, data) as response:
    assert response.data['email'] == 'billg@microsoft.com'
```

[Django]: https://www.djangoproject.com/
[Splunk]: http://dev.splunk.com/view/python-sdk/SP-CAAAEU2
