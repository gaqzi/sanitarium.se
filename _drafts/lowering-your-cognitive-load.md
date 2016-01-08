---
author: björn
comments: true
date: 2016-01-08 20:00:00 +08:00
layout: post
slug: lowering-your-cognitive-load
title: Lowering your cognitive load
subtitle: A take on why conformity is good
categories:
- blog
tags:
- rant
- programming
- opinion
---
As developers we all have to keep a lot of things in our heads as we work out
problems. To be able to focus on the *actual* problem that is being solved we
use descriptive names, conventions, best practices and follow coding standards.

All of these are there to in some way help us write code better. Maybe it's to
show intent (naming), or being consistent so others can guess how to use your
interface (convention), or quoting inputs from users (best practice), or not
letting your lines run 200 characters wide [PEP8] (coding standard).

When coding Python I'm adamant about following PEP8. I'm not perfect, but I
try. The benefit from following it far outweighs not doing it. **It means I can
focus on what the code is doing.** 
It's a bit like how they explained how they follow along in [The Matrix]:

> …there's way too much information to decode the Matrix. 
> You get used to it, though. Your brain does the translating. 
> I don't even see the code. All I see is blonde, brunette, redhead.

When I see `if is_valid_email(user.email):` I can be sure my user's email
address was just verified. Because the convention in Python is that `is_`
returns a boolean, and the name did the rest. But I must admit that the
equivalent `valid_email?(user.email)` in Ruby is a lot prettier.

Or in [Django] when using [class based views] I know that a method like
`get_redirect_url` will be configurable by:

 1. Defining the class attribute `redirect_url`
 2. By overriding the implementation in my class `get_redirect_url`

This might seem like a small thing. But knowing I can provide a static override
easily as well as a dynamic for when I need the flexibility is great. Sure,
maybe not the cleanest interface. But it's consistent and really useful.

# Code smell

One of my favorite things by following these patterns and standards is that
they can help sniff out smells. For example by instantiating all your class
attributes in the class definition or your `__init__` you can see when your
class is getting too big.

I was doing a code review and saw a warning for exactly this issue. I asked the
developer why they hadn't put it in `__init__` or directly on the class and the
answer basically boiled down to, "It kinda smelled". Shovel, meet carpet.
 
A contrived example:

```python
class Car:
    def insert_key(self, key):
        self.key = key
    
    def turn_key(self, to):
         # …
    
    def start(self):
        self.turn_key('on')
    

```

got warnings that attributes was being assigned for the first time in other methods than
`__init__`. Talking with the developer that had done that I got the response
that it looks bad to move them all to `__init__` or set them directly on the
class. Doing that, they felt, gave it a smell. 

## An aside

One big pet peeve of mine is people that are using single and double quotes
inconsistently. I don't really care which one you use. I have my preference,
but whatever. Just start with the current line, be consistent on that. Then the
method/function, the class, and then finally the whole file and project. 

Programming is a profession of precision. If you're inconsistent about small
inconsequential things like this I'm not sure why I should trust you to
implement bigger things.

